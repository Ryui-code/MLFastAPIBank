from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

app = FastAPI()

model = joblib.load('model (2).pkl')
scaler = joblib.load('scaler (2).pkl')

education_list = ['Bachelor', 'Doctorate', 'High School', 'Master']
home_ownership_list = ['OTHER', 'OWN', 'RENT']
loan_intent_list = ['EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE']

class BankSchema(BaseModel):
    person_age: int
    person_income: int
    person_emp_exp: int
    loan_amnt: int
    loan_int_rate: int
    loan_percent_income: int
    cb_person_cred_hist_length: int
    credit_score: int
    person_gender: str
    person_education: str
    person_home_ownership: str
    loan_intent: str
    previous_loan_defaults_on_file: str

def build_features(b: BankSchema):

    numeric = [
        b.person_age,
        b.person_income,
        b.person_emp_exp,
        b.loan_amnt,
        b.loan_int_rate,
        b.loan_percent_income,
        b.cb_person_cred_hist_length,
        b.credit_score,
    ]

    gender = [1 if b.person_gender == 'male' else 0]

    education = [1 if b.person_education == e else 0 for e in education_list]

    home_ownership = [1 if b.person_home_ownership == h else 0 for h in home_ownership_list]

    loan_intent = [1 if b.loan_intent == l else 0 for l in loan_intent_list]

    prev_default = [1 if b.previous_loan_defaults_on_file == 'Yes' else 0]

    return (
        numeric
        + gender
        + education
        + home_ownership
        + loan_intent
        + prev_default
    )

@app.post('/predict/')
async def predict(bank: BankSchema):
    features = build_features(bank)
    scaled = scaler.transform([features])

    pred = model.predict(scaled)[0]
    prob = model.predict_proba(scaled)[0][1]

    return {
        'approved': bool(pred),
        'probability': float(prob)
    }

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)