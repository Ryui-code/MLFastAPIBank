from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib

app = FastAPI()

model = joblib.load('model (2).pkl')
scaler = joblib.load('scaler (2).pkl')

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

@app.post('/predict/')
async def predict(bank: BankSchema):
    bank_dict = bank.dict()

    new_gender = bank_dict.pop('person_gender')
    gender1or_0 = [
        1 if new_gender == 'male' else 0
    ]

    new_cb = bank_dict.pop('previous_loan_defaults_on_file')
    cb1or_0 = [
        1 if new_cb == 'Yes' else 0
    ]

    new_edu = bank_dict.pop('person_education')
    edu1or_0 = [
        1 if new_edu == 'Bachelor' else 0,
        1 if new_edu == 'Doctorate' else 0,
        1 if new_edu == 'High School' else 0,
        1 if new_edu == 'Master' else 0,
    ]

    new_pho = bank_dict.pop('person_home_ownership')
    pho1or_0 = [
        1 if new_pho == 'OTHER' else 0,
        1 if new_pho == 'OWN' else 0,
        1 if new_pho == 'RENT' else 0
    ]

    new_loani = bank_dict.pop('loan_intent')
    loani1or_0 = [
        1 if new_loani == 'EDUCATION' else 0,
        1 if new_loani == 'HOMEIMPROVEMENT' else 0,
        1 if new_loani == 'MEDICAL' else 0,
        1 if new_loani == 'PERSONAL' else 0,
        1 if new_loani == 'VENTURE' else 0
    ]

    features = list(bank_dict.values()) + gender1or_0 + cb1or_0 + edu1or_0 + pho1or_0 + loani1or_0

    scaled_data = scaler.transform([features])
    approved = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0][1]

    return {
        "approved": bool(approved),
        "probability": float(probability)
    }

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)