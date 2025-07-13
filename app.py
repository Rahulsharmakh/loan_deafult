from flask import Flask, request, render_template
import requests
import os


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs
        age = int(request.form['Age'])
        income = float(request.form['Income'])
        loan_amount = float(request.form['LoanAmount'])
        credit_score = int(request.form['CreditScore'])
        months_employed = int(request.form['MonthsEmployed'])
        num_credit_lines = int(request.form['NumCreditLines'])
        interest_rate = float(request.form['InterestRate'])
        loan_term = int(request.form['LoanTerm'])
        dti_ratio = float(request.form['DTIRatio'])

        education = request.form['Education']
        employment_type = request.form['EmploymentType']
        marital_status = request.form['MaritalStatus']
        has_mortgage = request.form['HasMortgage']
        has_dependents = request.form['HasDependents']
        loan_purpose = request.form['LoanPurpose']
        has_co_signer = request.form['HasCoSigner']

        # Prepare JSON to send to Hugging Face
        data = {
            "Age": age,
            "Income": income,
            "LoanAmount": loan_amount,
            "CreditScore": credit_score,
            "MonthsEmployed": months_employed,
            "NumCreditLines": num_credit_lines,
            "InterestRate": interest_rate,
            "LoanTerm": loan_term,
            "DTIRatio": dti_ratio,
            "Education": education,
            "EmploymentType": employment_type,
            "MaritalStatus": marital_status,
            "HasMortgage": has_mortgage,
            "HasDependents": has_dependents,
            "LoanPurpose": loan_purpose,
            "HasCoSigner": has_co_signer
        }

        # 🔁 Replace this with your actual Hugging Face Space URL
        api_url = "https://rahul151004-loan-default-clf.hf.space/predict"


        # Send request
        response = requests.post(api_url, json=data)
        response.raise_for_status()

        # Extract result
        result_data = response.json()
        result = result_data.get("result", "Something went wrong.")
        prediction = result_data.get("prediction", -1)
        confidence_percent = result_data.get("confidence", 0)

    except Exception as e:
        result = f"Prediction failed. Error: {str(e)}"
        prediction = -1
        confidence_percent = 0

    return render_template(
        'result.html',
        prediction_text=result,
        prediction_class=prediction,
        confidence=confidence_percent
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
