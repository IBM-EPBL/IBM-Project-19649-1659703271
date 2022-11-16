import numpy as np
import os
from PIL import Image
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename, redirect
from gevent.pywsgi import WSGIServer
from flask import send_from_directory
from joblib import Parallel,delayed
import joblib
import pandas as pd
from scipy.sparse import ISSPARSE
import pickle
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "yjJRKquYkWeXxU3CGuvFC0Q1f29M8lpidj6PZ8B0RQgY"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/result', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        lend_data = request.form.get('lend')
        data = [[request.form.get('gender'),request.form.get('married'),request.form.get('dep'),request.form.get('edu'),request.form.get('se'),request.form.get('ai')
                ,request.form.get('cai'),request.form.get('la'),request.form.get('lat'),request.form.get('ch'),request.form.get('pa')]]
  
       
        a=''
        lend_data=int(lend_data)

        data_list = data.tolist()

        payload_scoring = {"input_data": [{"fields": ['gender','married','depend','education','self_emp','applicant_income','co_income','loan_amount','loan_term','credit_history','property_area'], "values": data_list}]}

        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/20aab57d-c8a0-48e0-bf79-b48bac4f7de3/predictions?version=2022-11-16', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
        print("response_scoring")
        prediction = response_scoring.json()
        num = prediction['predictions'][0]['values'][0][0]

        if(num==0):
            if(lend_data==1):
                a='It is not advisable to provide loan for this applicant.'
            else:
                a='Your Loan application will be Rejected.'
        else:
            if(lend_data==1):
                a='This applicant can be provided with the loan amount requested.'
            else:
                a='Your Loan application will be succesfull.'
        return render_template('submit.html', num=a)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
