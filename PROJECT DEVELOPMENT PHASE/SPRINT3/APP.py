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
from scipy.sparse import issparse



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
  
        df = pd.DataFrame(data, columns=['Gender','Married','Dependents','Education',
                                         'Self_Employed','ApplicantIncome','CoapplicantIncome',
                                         'LoanAmount','Loan_Amount_Term','Credit_History','Property_Area'])

        gh=joblib.load('/Users/hariharanganesh/Downloads/IBM/PROJECT/rdf.pkl')
        num=gh.predict(df)
        a=''
        lend_data=int(lend_data)
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
