# an object of WSGI application

from flask import Flask, flash,redirect,render_template,request,url_for
from wtforms import Form, FloatField, validators
import sqlite3
import cgi
import webbrowser
import jinja2
from datetime import datetime
import os
import pytz
import requests
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#app = Flask(__name__, template_folder='Onay\PycharmProjects\OnlineBondApp\templates', static_folder='Onay\PycharmProjects\OnlineBondApp\static')  # Flask constructor

app= Flask(__name__)  # Flask constructor

# A decorator used to tells the application
# which URL is associated function
@app.route('/',methods=['POST','GET'])
def index():
      return '''
      
<!DOCTYPE html>
<html lang="en" dir="ltr">
 
<head>
    <meta charset="utf-8">
    <title>Python Flask Mortgage Calculator</title>
 
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
    <link href="../static/signup.css" rel="stylesheet"> 
 
</head>
 
<body>
 
    <div class="container">
        <div class="header">
            <nav>

            </nav>
            <h3 class="text-muted">Python Flask App</h3>
        </div>
 
        <div class="jumbotron">
            <h1>Online Mortgage Bond App</h1>
            <p class="lead"></p>
            <p><a class="btn btn-lg btn-success" href="{{ url_for('student',filename='student.html') }}" role="button">Get bond estimate</a>
            </p>
        </div>
 
        <div class="row marketing">
            <div class="col-lg-6">
                <h4>Previous Mortgage quotes</h4>
                
                <h4>Bucket List</h4>
                <h4>
               </h4>
               
            </div>
        </div>
                <h4>

               </h4> 

        <footer class="footer">
            <p>&copy; Company 2019</p>
        </footer>
 
    </div>
</body>
 
</html>
      '''

# Model
class  InputForm(Form):
    Purchase_Price = FloatField(label='Price($)', validators=[validators.InputRequired()])
    Deposit_Paid=FloatField(label='Deposit($)',validators=[validators.InputRequired()])
    Bond_Term=FloatField(label='Term(Years)',validators=[validators.InputRequired()])
    Fixed_Interest_Rate=FloatField(label='IR(%)', validators=[validators.InputRequired()])

#@app.route('/')
#@app.route('/student',methods=['POST','GET'])
#def student():
#    return render_template('student.html')
#    return redirect(url_for(student))

#@app.route('/result',methods=['POST','GET'])
#def result():
#    if request.method=='POST':
#        result=request.form
#        return render_template("result.html",result=result, error=error)
# View
@app.route('/result', methods=['GET', 'POST'])
def result():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        Purchase_Price = form.Purchase_Price.data
        Deposit_Paid = form.Deposit_Paid.data
        Bond_Term = form.Bond_Term.data
        Fixed_Interest_Rate=form.Fixed_Interest_Rate.data

        Purchase_Price=request.form['Purchase_Price']
        Deposit_Paid=request.form['Deposit_Paid']
        Bond_Term=request.form['Bond_Term']
        Fixed_Interest_Rate=request.form['Fixed_Interest_Rate']

        Bond_Term1=(12*Bond_Term)
        R=1+float(Fixed_Interest_Rate)*(0.12)
        X=(Purchase_Price*((1-Deposit_Paid)*0.01))*(R**Bond_Term1)*(1-R)/(1-R**Bond_Term1)
        Monthly_Interest=[]
        Monthly_Balance=[]
        for i in range(1,Bond_Term1+1):
            Interest=(Purchase_Price*((1-Deposit_Paid)*0.01))*(R-1)
            Loan_Amount=(Purchase_Price*((1-Deposit_Paid)*0.01))-(X-Interest)
            Monthly_Interest=np.append(Monthly_Interest,Interest)
            Monthly_Balance=np.append(Monthly_Balance,Loan_Amount)

        # Produce Visualization of Monthly Loan Balance and Interest
        plt.plot(range(1,Bond_Term1+1),Monthly_Interest,'r',lw=2)
        plt.xlabel('month')
        plt.ylabel('monthly interest ($)')
        #        plt.show()
        plt.savefig('Monthly Loan interest.png')
        plt.plot(range(1,Bond_Term1+1),Monthly_Balance,'b',lw=2)
        plt.xlabel('month')
        plt.ylabel('monthly loan balance ($)')
        #        plt.show()
        plt.savefig('Monthly Loan Balance.png')


        return render_template("result.html", form=form, Monthly_Interest=Monthly_Interest, Monthly_Balance=Monthly_Balance, Purchase_Price=Purchase_Price, Deposit_Paid=Deposit_Paid, Bond_Term=Bond_Term, Fixed_Interest_Rate=Fixed_Interest_Rate)
    else:
        return render_template("index.html", form=form)

if __name__=='__main__':
    app.run(debug = True)
