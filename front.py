import streamlit as st
import requests

api = 'http://127.0.0.1:8000/predict/'

st.title('Bank Project')

person_age = st.number_input('Age', min_value=18.0, max_value=100.0, step=1.0)

person_income = st.number_input('Person income', min_value=0.0, step=1000.0)

person_emp_exp = st.number_input('Experience', min_value=0.0, step=1.0)

loan_amnt = st.number_input('Loan amount score', min_value=0.0, step=100.0)

loan_int_rate = st.number_input('Loan intent rate', min_value=0.0, step=1.0)

loan_percent_income = st.number_input('Loan percent income', min_value=0.0, step=500.0)

cb_person_cred_hist_length = st.number_input('Credit history length', min_value=0.0, step=1.0)

credit_score = st.number_input('Credit score', min_value=0.0, step=10.0)

person_gender = st.selectbox('Gender', ['Male', 'Female'])

person_education = st.selectbox('Education', ['Bachelor', 'Doctorate', 'High School', 'Master', 'Associate'])

person_home_ownership = st.selectbox('Home Ownership', ['OTHER', 'OWN', 'RENT', 'MORTGAGE'])

loan_intent = st.selectbox('Loan intent', ['EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE', 'DEBTCONSOLIDATION'])

previous_loan_defaults_on_file = st.selectbox('Default', ['Yes', 'No'])

bank_data = {
    'person_age': person_age,
    'person_income': person_income,
    'person_emp_exp': person_emp_exp,
    'loan_amnt': loan_amnt,
    'loan_int_rate': loan_int_rate,
    'loan_percent_income': loan_percent_income,
    'cb_person_cred_hist_length': cb_person_cred_hist_length,
    'credit_score': credit_score,
    'person_gender': person_gender,
    'person_education': person_education,
    'person_home_ownership': person_home_ownership,
    'loan_intent': loan_intent,
    'previous_loan_defaults_on_file': previous_loan_defaults_on_file
}

if st.button('Check'):
    try:
        request = requests.post(api, json=bank_data, timeout=10)
        if request.status_code == 200:
            result = request.json()
            st.json(result)
        else:
            st.error(f'Error: {request.status_code}')
    except requests.exceptions.RequestException as e:
        st.error(f'Can not connect to the API')