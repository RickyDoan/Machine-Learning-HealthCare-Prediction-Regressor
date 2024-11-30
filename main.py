import streamlit as st
import pandas as pd
from predict_db import predict_db

st.title("The Health Care Premium Prediction App")

# Row 1: Age, Number of Dependants, Income_USD
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=15, max_value=72, step=1, value=15)
with col2:
    insurance_plan = st.selectbox("Insurance Plan", ['Input Insurance Plan', 'Gold', 'Silver', 'Bronze'])

with col3:
    medical_history = st.selectbox("Medical History", ["Input History", 'No Disease',
                                                       'High blood pressure', 'Thyroid',
                                                       'High blood pressure & Heart disease', 'Diabetes & Thyroid',
                                                       'Diabetes', 'Heart disease', 'Diabetes & High blood pressure',
                                                       'Diabetes & Heart disease'
                                                       ])
# Row 2: Insurance Plan, Gender, Region
col4, col5, col6 = st.columns(3)
with col4:
    number_of_dependants = st.number_input("Number Of Dependants", min_value=0, max_value=5, step=1, value=2)
with col5:
    income_usd = st.number_input("Income (USD) Per Month", min_value=0, max_value=1000, step=1, value=700)
with col6:
    region = st.selectbox("Region", ['Southeast', 'Northeast', 'Southwest', 'Northwest'])

# Row 3: Marital Status, Physical Activity, Stress Level
col7, col8, col9 = st.columns(3)
with col7:
    marital_status = st.selectbox("Marital Status", ['Married', 'Unmarried'])
with col8:
    physical_activity = st.selectbox("Physical Activity", ['Low','Medium', 'High'])
with col9:
    stress_level = st.selectbox("Stress Level", ['High', 'Medium',  'Low'])

# Row 4: Medical History, BMI Category, Smoking Status
col10, col11, col12 = st.columns(3)
with col10:
    gender = st.selectbox("Gender", ['Male', 'Female'])
with col11:
    bmi_category = st.selectbox("BMI Category",
                                ['Overweight', 'Normal',  'Obesity', 'Underweight'])
with col12:
    smoking_status = st.selectbox("Smoking Status", ['Occasional','No Smoking',  'Regular'])

# Row 5: Employment Status
col13, _, _ = st.columns([1, 1, 1])
with col13:
    employment_status = st.selectbox("Employment Status",
                                     ['Self-Employed', 'Freelancer', 'Salaried'])

list_input = {
    'Age': age,
    'Number Of Dependants': number_of_dependants,
    'Income (USD) Per Month': income_usd,
    'Insurance Plan': insurance_plan,
    'Gender': gender,
    'Region': region,
    'Marital Status': marital_status,
    'Physical Activity': physical_activity,
    'Stress Level': stress_level,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Employment Status': employment_status,
    'Medical History': medical_history,
}


# Display the collected information (Optional)
if 'first_click' not in st.session_state:
    st.session_state.first_click = True  # Track first click

if st.button("Submit"):
    input_yet = []

    if insurance_plan == 'Input Insurance Plan':
        input_yet.append('Please which INSURANCE PLAN would you like?')
    if age == 15:
        input_yet.append('And tell me your AGE ?')
    elif medical_history == 'Input History':
        input_yet.append('And the last : Your MEDICAL HISTORY')

    if input_yet:
        if len(input_yet) == 3:
            st.warning(f"Please fill Insurance Plan, Age, and Medical History.")
        else:
            st.warning(f"{' '.join(input_yet)}")
    else:
        # Get the prediction result
        call = predict_db(list_input)
        st.success(call)

        # Show the message only the first time
        if st.session_state.first_click:
            st.success("Play around with the inputs to see what changes!")
            st.session_state.first_click = False

