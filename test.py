import requests

response = requests.get("http://127.0.0.1:5000/getMedicalInfo", params={"abha_id": "ABHA123456"})

# Ensure the response is valid JSON
if response.status_code == 200:
    try:
        data = response.json()  # Extract the JSON response
        print(data)  # Print the entire JSON for debugging

        # Access patient details
        patient_details = data.get('Patient Details', {})
        age = int(patient_details.get('Age', 0))  # Default to 0 if 'Age' is missing
        medical_info = data.get('Medical Information', {})
        prcondition = medical_info.get('Condition', "N/A")  # Default to "N/A"
        prlab = medical_info.get('LabResults', "N/A")  # Default to "N/A"
        prmed = medical_info.get('Medications', "N/A")  # Default to "N/A"

        print(prlab, prmed, prcondition)
    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
else:
    print(f"Failed to get data. HTTP status code: {response.status_code}")
