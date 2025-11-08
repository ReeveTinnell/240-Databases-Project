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

@app.route('/viewTable', methods=['GET'])
def viewTable():

    table = request.args.get('table')

    output = render_template('viewTable.html', table=table, attributes=attributes)
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

@app.route('/addCompany', methods=['POST'])
def addCompanyToList():

    new_company = [
        request.form['name'],
        request.form['industry'],
        request.form['location'],
        request.form['size'],
        request.form['website']
        ]

    addTo("company", new_company)

    return redirect(url_for('viewCompanies'))

@app.route('/deleteCompany')
def deleteCompany():
    output = render_template('deleteCompany.html')
    return output

@app.route('/deleteCompany', methods=['POST'])
def deleteCompanyFromTable():

    id = request.form['id']
    name = request.form['name']

    error = None

    company = getEntry("company", id)

    if len(company) == 0:
        error="ERROR! No company found, please enter a correct company id"
        output = render_template('deleteCompany.html', error=error)
        return output
    if company[0][1] != name:
        error="ERROR! Company name does not match company name file"
        output = render_template('deleteCompany.html', error=error)
        return output
    else:
        delFrom("company", id)
        return redirect(url_for('viewCompanies'))

@app.route('/updateCompany')
def updateCompany():
    output = render_template('updateCompany.html')
    return output


@app.route('/updateCompany', methods=['POST'])
def updateCompanyEntry():

    id = request.form['id']

    update_values = [
        request.form['name'],
        request.form['industry'],
        request.form['location'],
        request.form['size'],
        request.form['website']
        ]

    updateEntry("company", id, update_values)

    return redirect(url_for('viewCompanies'))


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
