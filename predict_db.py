

import streamlit as st
import pandas as pd
from joblib import load
from sklearn.preprocessing import MinMaxScaler

best_model = load("artifact/best_model.joblib")
scaler_object = load("artifact/scaler.joblib")

Physical_Activity = {
    'High': 0,
    'Medium': 1,
    'Low': 4
}
Stress_Level = {
    'High': 4,
    'Medium': 1,
    'Low': 0
}
risk_scores = {
    "diabetes": 6,
    "heart disease": 8,
    "high blood pressure": 6,
    "thyroid": 5,
    "no disease": 0,
    "None": 0
}


def physical_activity(physical_activity, stress_level):
    physical = Physical_Activity.get(physical_activity, 0)
    stress = Stress_Level.get(stress_level, 0)
    total_risk = physical + stress
    min_score = 0
    max_score = 8
    life_style_risk = (total_risk - min_score) / (max_score - min_score)
    return life_style_risk


def risk_disease(medical_history):
    diseases = medical_history.lower().split(" & ")
    total_risk = sum(risk_scores.get(disease, 0) for disease in diseases)
    max_score = 14
    min_score = 0
    total_risk_disease = (total_risk - min_score) / (max_score - min_score)
    return total_risk_disease


def processing_input(list_input):
    list_columns = ['Age', 'Number Of Dependants', 'Insurance_Plan', 'Income_USD',
                    'life_style_risk', 'total_risk_disease', 'Gender_Male',
                    'Region_Northwest', 'Region_Southeast', 'Region_Southwest',
                    'Marital_status_Unmarried', 'BMI_Category_Obesity',
                    'BMI_Category_Overweight', 'BMI_Category_Underweight',
                    'Smoking_Status_Occasional', 'Smoking_Status_Regular',
                    'Employment_Status_Salaried', 'Employment_Status_Self-Employed']

    df = pd.DataFrame(0, columns=list_columns, index=[0])

    insurance_plan = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    #'Gold', 'Silver', 'Bronze'
    df['life_style_risk'] = physical_activity(list_input['Physical Activity'], list_input['Stress Level'])
    df['total_risk_disease'] = risk_disease(list_input['Medical History'])
    for key, data in list_input.items():
        if key == 'Age':
            df['Age'] = data/100
        elif key == 'Number Of Dependants':
            #  'Number of Dependants': number_of_dependants,
            df['Number Of Dependants'] = data/100
        elif key == 'Insurance Plan':
            df['Insurance_Plan'] = (insurance_plan.get(data, 1))/3
        elif key == 'Income (USD) Per Month':
            df['Income_USD'] = data/1000
        elif key == 'Gender' and data == 'Male':
            df['Gender_Male'] = 1
        elif key == 'Region':
            if data == 'Northwest':
                df['Region_Northwest'] = 1
            elif data == 'Southeast':
                df['Region_Southeast'] = 1
            elif data == 'Southwest':
                df['Region_Southwest'] = 1
        elif key == ' Martial Status' and data == 'Unmarried':
            df['Martial_Status_Unmarried'] = 1
        elif key == 'BMI_Category':
            if data == 'Obesity':
                df['BMI_Category_Obesity'] = 1
            elif data == 'Underweight':
                df['BMI_Category_Underweight'] = 1
            elif data == 'Overweight':
                df['BMI_Category_Overweight'] = 1
        elif key == 'Smoking Status':
            if data == 'Occasional':
                df['Smoking_Status_Occasional'] = 1
            elif data == 'Regular':
                df['Smoking_Status_Regular'] = 1
        elif key == 'Employment Status':
            if data == 'Salaried':
                df['Employment_Status_Salaried'] = 1
            elif data == 'Self-Employed':
                df['Employment_Status_Self-Employed'] = 1
        df = handle_scaler(df)
    return df

def handle_scaler(df):
    # scaler = scaler_object['scaler']
    # list_scaler = scaler_object['list_scaler']
    # df['Income_Level'] = 0
    # df[list_scaler] = scaler.transform(df[list_scaler])
    # df.drop('Income_Level', axis=1, inplace=True)
    return df


def predict_db(list_input):
    prediction_input = processing_input(list_input)
    prediction = best_model.predict(prediction_input)
    return f"The annual insurance premium is about $  {str(int(prediction[0]))}"
