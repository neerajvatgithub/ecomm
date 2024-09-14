import openai
import json

# Make sure to replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = 'sk-proj-expOpqxZmNpZ2C0A1awgT3BlbkFJutnAo0YcByYk8phanuzY'


def summarize_json(json_input):
    # Convert the JSON input to a string
    json_string = json.dumps(json_input, indent=2)

    # Create a prompt for the OpenAI API
    # prompt = f"Summarize the following JSON data in 100 words:\n\n{json_string}\n\nSummary:"
    prompt = f"Summarize this in 200 words capturing all the elements of it:\n\n{json_string}\n\n"
    # Call the OpenAI API to get a summary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.0
    )

    # Extract the summary from the response
    summary = response['choices'][0]['message']['content'].strip()

    return summary


if __name__ == "__main__":
    # Example JSON input
    json_input = {
  "vitals": {
    "age": "2Y 1M 1D",
    "weight": "11 kg",
    "height": "90 cm",
    "body_surface_area": "0.52 m²",
    "BMI": "13.58"
  },
  "diagnoses": [
    {
      "condition": "Acquired stenosis of external ear canal secondary to inflammation and infection, bilateral",
      "details": "Acquired stenosis of external ear canal secondary to inflammation and infection, bilateral"
    },
    {
      "condition": "Acquired stenosis of external ear canal secondary to inflammation and infection, unspecified",
      "details": "Acquired stenosis of external ear canal secondary to inflammation and infection, unspecified"
    }
  ],
  "instructions": [
    "Avoid bananas",
    "Avoid deep fried items",
    "Avoid ice cold items",
    "Avoid chutneys",
    "Avoid achaar",
    "Avoid sauce items"
  ],
  "physical_examinations": {
    "CVS": "examined normal",
    "severity": "Moderate"
  },
  "notes": "Follow up after 3 days",
  "birth_history": {
    "date_of_birth": "17/04/2021",
    "time_of_birth": "05:30",
    "APGAR_score": "1 2 4",
    "mode_of_delivery": "NVD"
  },
  "doctor_details": {
    "name": "Testobg Oar",
    "qualifications": [
      "MBBS (BLDE Shri B M Patil Medical College, Dharwar University)",
      "DGO (Jagadguru Jayadeva Murugarajendra Medical College, 2005)",
      "Fellowship in Fetal Medicine (BFMC, Bangalore)"
    ],
    "contact_number": "999999",
    "office_address": "Opposite Kemp fort (Total Mall), Old Airport Road, Bengaluru 560017"
  }
}



    # Get the summary of the JSON input
    summary = summarize_json(json_input)

    # Print the summary
    print("Summary:", summary)
