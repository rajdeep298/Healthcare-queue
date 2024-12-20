import csv

try:
    with open('patient_abha.csv', mode='w', newline='') as patient_abha_file:
        writer = csv.writer(patient_abha_file)
        writer.writerow(["PatientID", "Name", "Age", "Gender", "ABHA_ID"])  # Added Age and Gender
        writer.writerows([
            ["P001", "Ramesh Kumar", "55", "Male", "ABHA123456"],  # Added Age and Gender
            ["P002", "Sita Verma", "42", "Female", "ABHA654321"],  # Added Age and Gender
            ["P003", "Amit Shah", "60", "Male", "ABHA987654"],  # Added Age and Gender
            ["P004", "Priya Mehta", "38", "Female", "ABHA456789"],  # Added Age and Gender
        ])
    print("File 'patient_abha.csv' created successfully.")
except Exception as e:
    print("Error creating 'patient_abha.csv':", e)

try:
    with open('medical_info.csv', mode='w', newline='') as medical_info_file:
        writer = csv.writer(medical_info_file)
        writer.writerow(["ABHA_ID", "Condition", "Medications", "LabResults", "LastVisitDate"])
        writer.writerows([
            ["ABHA123456", "Hypertension", "Amlodipine", "BP: 140/90", "2023-12-15"],
            ["ABHA654321", "Diabetes", "Metformin", "HbA1c: 7.2%", "2023-11-20"],
            ["ABHA987654", "Asthma", "Salbutamol", "Spirometry: Mild Obstruction", "2023-10-05"],
            ["ABHA456789", "No significant issues", "None", "All tests normal", "2023-12-01"],
        ])
    print("File 'medical_info.csv' created successfully.")
except Exception as e:
    print("Error creating 'medical_info.csv':", e)