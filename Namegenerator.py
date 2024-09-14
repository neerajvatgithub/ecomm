from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'sk-proj-expOpqxZmNpZ2C0A1awgT3BlbkFJutnAo0YcByYk8phanuzY'

# Use a raw string for the template folder path
template_dir = r'C:\Users\neerajv\PycharmProjects\pythonProject1'
app.template_folder = template_dir

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        letter = request.form['letter']
        gender = request.form['gender']
        names_with_meanings = generate_names(letter, gender)
        return render_template('index.html', names=names_with_meanings)
    return render_template('index.html')

def generate_names(letter, gender):
    prompt = f"Generate 5 Indian {gender} names starting with the letter '{letter}' along with their meanings in hindi and english. Format: Name: Meaning in hindi: Meaning in English"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that generates Indian {gender} names with their meanings."},
            {"role": "user", "content": prompt}
        ]
    )
    names_with_meanings = response.choices[0].message['content'].strip().split('\n')
    return names_with_meanings

if __name__ == '__main__':
    app.run(debug=True)