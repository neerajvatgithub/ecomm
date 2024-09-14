# app.py
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from PIL import Image
import requests
import json
import base64
import openai

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up OpenAI API key
openai.api_key = 'sk-proj-expOpqxZmNpZ2C0A1awgT3BlbkFJutnAo0YcByYk8phanuzY'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the image and identify food items
        food_items = identify_food_items(filepath)

        # Get calorie information
        calorie_info = get_calorie_info(food_items)

        return jsonify(calorie_info)
    return jsonify({'error': 'File type not allowed'})


def identify_food_items(filepath):
    # Read the image file
    with open(filepath, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the prompt for the LLM
    prompt = f"""Analyze the following image and identify the food items present:
    [IMAGE]{image_data}[/IMAGE]
    List only the food items you can see, separated by commas."""

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that identifies food items in images."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    # Extract the food items from the response
    food_items = response.choices[0].message['content'].strip().split(', ')
    return food_items


def get_calorie_info(food_items):
    # Prepare the prompt for the LLM
    items_list = ", ".join(food_items)
    prompt = f"""For the following food items: {items_list}
    Provide the estimated calorie count for each item and the total calorie count.
    Format your response as a JSON object with the following structure:
    {{
        "items": [
            {{"name": "item1", "calories": 100}},
            {{"name": "item2", "calories": 150}}
        ],
        "total_calories": 250
    }}"""

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that provides calorie information for food items."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    # Extract and parse the JSON response
    calorie_info = json.loads(response.choices[0].message['content'])
    return calorie_info


if __name__ == '__main__':
    app.run(debug=True)