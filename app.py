from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load the medicines dataset
medicines_df = pd.read_csv('data/medicines.csv')
patients_df = pd.read_csv('data/patients.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat.html', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        sex = request.form['sex']
        blood_group = request.form['blood_group']
        medical_history = ','.join(request.form.getlist('medical_history'))
        symptoms = request.form['symptoms']
        duration = request.form['duration']
        
        age_group = 'below_15' if age < 15 else 'above_15'
        
        recommended_medicine = medicines_df[(medicines_df['age_group'] == age_group) & 
                                            (medicines_df['symptom'].str.contains(symptoms, case=False))]

        if not recommended_medicine.empty:
            medicine = recommended_medicine.iloc[0]['medicine']
            dosage = recommended_medicine.iloc[0]['dosage']
        else:
            medicine = 'No suitable medicine found'
            dosage = 'N/A'

        # new_patient_data = {
        #     'name': name,
        #     'age': age,
        #     'sex': sex,
        #     'blood_group': blood_group,
        #     'medical_history': medical_history,
        #     'symptoms': symptoms,
        #     'duration': duration,
        #     'medicine_recommended': f'{medicine} {dosage}'
        # }

        # # Append new patient data to the patients.csv
        # patients_df = patients_df.append('data/patients.csv', ignore_index=True)
        # patients_df.to_csv('data/patients.csv', index=False)

        return render_template('recommendation.html', name=name, medicine=medicine, dosage=dosage)
    
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)

