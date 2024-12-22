import os
from transformers import pipeline
import re

# Suppress TensorFlow warnings and info logs (optional)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppresses info and warnings, keeps errors

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

import requests

# Replace with the actual URL of your server
url = 'http://localhost:5000/getMedicalInfo?abha_id=ABHA123456'

# Send a GET request to fetch the medical info
response = requests.get(url)

# with open("Speech-to-Text/summary.txt", "r") as file:
#     recCurr = file.read()



# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON into a dictionary
    data = response.json()

    # Extract age from the 'Patient Details' part of the response
    patient_details = data.get('Patient Details', {})
    age = int(patient_details.get('Age', None))
    prcondition = patient_details.get('Condition', None)
    prlab = patient_details.get('LabResults', None)
    prmed = patient_details.get('Medications', None)
    print(prlab,prmed,prcondition)



    # Print the age
    if age:
        print(f"The patient's age is: {age}")
    else:
        print("Age not found in the response.")
else:
    print(f"Error: Unable to fetch data (Status code: {response.status_code})")


# Define the priority labels based on medical conditions
labels = [
    "Critical Emergencies",
    "High-Urgency Conditions",
    "Moderate-Urgency Conditions",
    "Chronic Conditions",
    "Preventive and Screening Needs",
    "Minor or Self-Limiting Conditions"
]

# Define keywords for each priority
critical_keywords = ["heart attack", "cardiac arrest", "stroke", "severe burns", "septic shock"]
high_urgency_keywords = ["appendicitis", "perforated ulcer", "severe dehydration", "high fever", "preterm labor"]
moderate_urgency_keywords = ["pneumonia", "COPD exacerbation", "fractures", "acute psychosis"]
chronic_keywords = ["hypertension", "stable angina", "asthma", "chronic back pain", "epilepsy"]
preventive_keywords = ["vaccination", "cancer screening", "antenatal checkup", "TB testing"]
minor_keywords = ["common cold", "mild viral fever", "acne", "seasonal allergies","regular checkup"]


# Function to check for keywords and classify the priority
def classify_priority(record):
    record_lower = record.lower()

    # Check for keywords for each priority level
    if any(keyword in record_lower for keyword in critical_keywords):
        return "Critical Emergencies (Priority 1)"
    elif any(keyword in record_lower for keyword in high_urgency_keywords):
        return "High-Urgency Conditions (Priority 2)"
    elif any(keyword in record_lower for keyword in moderate_urgency_keywords):
        return "Moderate-Urgency Conditions (Priority 3)"
    elif any(keyword in record_lower for keyword in chronic_keywords):
        return "Chronic Conditions (Priority 4)"
    elif any(keyword in record_lower for keyword in preventive_keywords):
        return "Preventive and Screening Needs (Priority 5)"
    elif any(keyword in record_lower for keyword in minor_keywords):
        return "Minor or Self-Limiting Conditions (Priority 6)"
    else:
        return "Unclassified (Please Review)"


# Example records (previous and current symptoms)
recPrev = "The patient has a history of mild asthma, stable hypertension, and no known kidney issues."
#recCurr = "The patient is currently experiencing severe abdominal pain, nausea, and vomiting. The physician suspects acute appendicitis and recommends surgical intervention."


# Combine previous and current records for classification
combined_record = f"Previous Record: {recPrev} Current Record: {recCurr}"

print("Running the classification...")

# Perform zero-shot classification using Hugging Face's model
try:
    # Check the priority classification based on combined records
    priority = classify_priority(combined_record)
    #print(priority)
    match = re.search(r"Priority (\d+)", priority)
    priority_value = int(match.group(1))
    priority_value=7-priority_value
    #print(f"The extracted priority value is: {priority_value}")
    if 0 <= age <= 2:
        priority_value+=0.99
    elif  3<= age <= 5:
        priority_value += 0.9
    elif 6 <= age <= 12:
        priority_value += 0.8
    elif  13<= age <= 18:
        priority_value += 0.7
    elif  19<= age <= 40:
        priority_value += 0.6
    elif  41<= age <= 64:
        priority_value += 0.89
    elif  age >= 65:
        priority_value += 0.9

    print(f"Priority based on keywords: {priority_value}")

    # Running the zero-shot classification to validate priority using model
    result = classifier(combined_record, candidate_labels=labels)
    print("Zero-shot Classification Result:")
    print(result)

except Exception as e:
    print(f"Error: {e}")

