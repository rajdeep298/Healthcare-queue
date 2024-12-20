from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Get the current directory where server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load patient data from CSV
def load_patient_data():
    patients = {}
    try:
        patient_file_path = os.path.join(BASE_DIR, '..', 'abha_database', 'patient_abha.csv')
        with open(patient_file_path, mode='r') as patient_abha_file:
            reader = csv.DictReader(patient_abha_file)
            for row in reader:
                patients[row['ABHA_ID']] = row
    except FileNotFoundError:
        print("Error: 'patient_abha.csv' not found.")
    return patients

# Load medical information from CSV
def load_medical_info():
    medical_info = {}
    try:
        medical_file_path = os.path.join(BASE_DIR, '..', 'abha_database', 'medical_info.csv')
        with open(medical_file_path, mode='r') as medical_info_file:
            reader = csv.DictReader(medical_info_file)
            for row in reader:
                medical_info[row['ABHA_ID']] = row
    except FileNotFoundError:
        print("Error: 'medical_info.csv' not found.")
    return medical_info

patients = load_patient_data()
medical_info = load_medical_info()

@app.route('/getMedicalInfo', methods=['GET'])
def get_medical_info():
    abha_id = request.args.get('abha_id')
    if not abha_id:
        return jsonify({"error": "ABHA ID is required"}), 400

    if abha_id in medical_info:
        patient_data = patients.get(abha_id, {})
        medical_data = medical_info[abha_id]

        response = {
            "Patient Details": patient_data,
            "Medical Information": medical_data
        }
        print(response)
        return jsonify(response)
    else:
        return jsonify({"error": "No medical information found for the given ABHA ID"}), 404

if __name__ == '__main__':
    app.run(debug=True)
