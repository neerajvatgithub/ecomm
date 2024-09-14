import openai
import json
import sys

# Make sure to replace 'your-openai-api-key' with your actual OpenAI API key
# openai.api_key = 'sk-proj-expOpqxZmNpZ2C0A1awgT3BlbkFJutnAo0YcByYk8phanuzY'

openai.api_key = "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"

def summarize_json(json_input):
    # Convert the JSON input to a string
    json_string = json.dumps(json_input, indent=2)

    # Create a prompt for the OpenAI API
    # prompt = f"Summarize the following JSON data in 100 words:\n\n{json_string}\n\nSummary:"
    # prompt = f"Summarize all the patient data like: patient 1: summary, patient2:summary, patient3:summary in paragraph capturing all the main elements of it. Add new line after each patient:\n\n{json_string}\n\n"
    # prompt = f"Summarize all the patient data capturing all the main elements of it. Word Limit 200 for each patient, each patient data in new line and output should a paragraph:\n\n{json_string}\n\n"
    prompt = f"Can you generate summary in 100 words. Do not leave any crucial details of the patient focusing on patient details, vitals, symptoms, and the course of action taken by doctors along with the doctor’s name for the given patient in paragraph format. Use the patient's name from the latest prescription. Ensure the summary is in chronological order by consultation date.\n\n{json_string}\n\n"
    # prompt = f"" \n\n{json_string}\n\n"

    # Call the OpenAI API to get a summary
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.0
    )

    # Extract the summary from the response
    summary = response['choices'][0]['message']['content'].strip()

    return summary


if __name__ == "__main__":
    # Example JSON input
    json_input = [
  {
    "name": "B/O Sanchayita Das",
    "age_gender": "5M 21D, Female",
    "mpid": "1000000101850580",
    "consultation_date": "27-02-2024, 02:44 pm",
    "weight": "6.16 kg",
    "symptoms": [
      "loose stools",
      "passing 6x per day since 3 days",
      "active, no dullness",
      "no reduction urine output",
      "no vomiting",
      "no fever"
    ],
    "notes": [
      "Enterogermina - 1 vial once a day for 7 days",
      "Z & D drops - 0.5ml once a day for 1 week",
      "Review in 3 days",
      "Colicaid drops - 0.7ml SOS (can be thrice a day)"
    ],
    "doctor": {
      "name": "Dr Sampat Kumar Shettigar",
      "qualifications": [
        "MBBS",
        "MD (Paediatrics)",
        "Fellowship - National Neonatology Forum",
        "Fellowship RCPCH-UK from London",
        "PGPN from the Boston University, USA"
      ],
      "kmc": "89574"
    },
    "office_address": "Nagarjuna Sai Signet, 2nd Floor, Plot no.11, Survey No. 88, Whitefield Main Road, Bengaluru 560066"
  },
  {
    "name": "B/O Sanchayita Das",
    "age_gender": "9M 12D, Female",
    "mpid": "1000000101850580",
    "consultation_date": "18-06-2024, 04:19 pm",
    "height": "71 cm",
    "weight": "7.28 kg",
    "bmi": "14.44 kg/m²",
    "ofc": "44 cm",
    "temperature": "98.2 °F",
    "bsa": "0.38 m²",
    "symptoms": "Vaccination visit",
    "assessments": "ROUTINE EXAMINATION AND VACCINATION",
    "notes": [
      "Trisevac + OPV Vaccination",
      "Calpol drops 1ml sos for fever",
      "Vitamin D 1ml once a day till 1 year",
      "Orofer XT drops 0.8ml once a day daily/alternate days in between the two meals till 1 year",
      "Nasavion saline nasal drops 2-2 drops in both the nostrils 5-6 times a day sos for nasal blockage",
      "Colicaid drops 0.8ml sos for colic",
      "Next vaccination at 1 year",
      "Review sos"
    ],
    "doctor": {
      "name": "Dr Ankur Rajvanshi",
      "qualifications": [
        "MD (Pediatrics)",
        "Fellowship in Neonatology FIPPN (Australia)"
      ],
      "kmc": "0000052"
    },
    "office_address": "Nagarjuna Sai Signet, 2nd Floor, Plot no.11, Survey No. 88, Whitefield Main Road, Bengaluru 560066"
  },
  {
    "name": "Aryahi",
    "age_gender": "10M 29D, Female",
    "mpid": "1000000101850580",
    "consultation_date": "05-08-2024, 12:55 pm",
    "birth_history": {
      "place_of_birth": "Cloudnine Whitefield IP",
      "date_of_birth": "06-09-2023",
      "time_of_birth": "04:09 pm",
      "mother_name": "Sanchayita Das",
      "mother_blood_group": "O+",
      "birth_weight": "3.01 Kg",
      "discharge_weight": "2.72 Kg",
      "gestation_age": "full term",
      "apgar_score": "8 9 10",
      "mode_of_delivery": "lscs"
    },
    "notes": [
      "babygesic drops 0.8ml 6th hrly",
      "Syp meftal p 2ml 3 times/day if temp 101°F or more",
      "Sinarest af drops 0.5ml 3 times/day for 5 days - cold",
      "mucolite drops 0.5ml 3 times/day for 5 days - cough",
      "advent drops 0.6ml 3 times/day for 5 days - after feed",
      "cereals stage 1"
    ],
    "doctor": {
      "name": "Dr Mohit Singhal",
      "qualifications": [
        "MBBS",
        "MD (DNB Neonatalogy)",
        "Fellowship in PGPN Boston USA"
      ],
      "kmc": "0000018"
    },
    "office_address": "Nagarjuna Sai Signet, 2nd Floor, Plot no.11, Survey No. 88, Whitefield Main Road, Bengaluru 560066",
    "contact_info": {
      "phone": "+91-9972999729",
      "email": "appsupport@cloudninecare.com"
    }
  }
]



    # Get the summary of the JSON input
    summary = summarize_json(json_input)

    # # Print the summary
    # print("Summary:", summary)



    # Save the original stdout
    original_stdout = sys.stdout

    # Redirect stdout to a file
    with open('output.txt', 'w') as f:
        sys.stdout = f
        print("Summary:", summary)
