#! /usr/bin/python3

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from models import *

app = Flask(__name__) # creates a flask application object

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

# example database uri = "mysql+pymysql://jeff:mypass@localhost/sakila"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}/{creds['db']}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def showCompanies():
    print("\n")
    companies = Company.query.all()
    for company in companies:
        print(f"[{company.id}] -> {company.name}")
    print("\n")


menuText = """Please select one of the following options:
1) Display company
2) Add a company
q) quit
"""



if __name__ == '__main__':
    with app.app_context():
        menuOption = ""
        while menuOption != 'q':
            menuOption = input(menuText)
            if menuOption == "1":
                showCompanies()
#    app.run(port=8000, debug=True, host="0.0.0.0")

