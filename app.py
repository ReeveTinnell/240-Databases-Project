#! /usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()
from menu_testing import *

def getConnection():
    connection = mysql.connector.connect(
        host=os.getenv('SQL_HOST'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PWD'),
        db=os.getenv('SQL_DB')
    )
    return connection


app = Flask(__name__)

@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/about')
def about():
    return(render_template('about.html'))

@app.route('/premade')
def premade():
    output = render_template('static.html')
    return output

@app.route('/companies')
def viewCompanies():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute(f"SELECT * FROM company")
    companies = myCursor.fetchall()
    output = render_template('viewCompanies.html', companies=companies)
    return output

@app.route('/addCompany')
def addCompany():
    output = render_template('addCompany.html')
    return output

@app.route('/addCompanyToList', methods=['GET'])
def addCompanyToList():

    new_company = [
        request.args.get('name'),
        request.args.get('industry'),
        request.args.get('location'),
        request.args.get('size'),
        request.args.get('website')
        ]
    print(new_company)
    addTo("company", new_company)

    return redirect(url_for('viewCompanies'))

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
