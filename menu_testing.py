#!/usr/bin/env python3

import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()

def getConnection():
    connection = mysql.connector.connect(
        host=os.getenv('SQL_HOST'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PWD'),
        db=os.getenv('SQL_DB')
    )
    return connection

""" company = {name, industry, website, location, size}
contact = {name, email, phone, position}
job = {title, post_date, close_date, hyperlink}
fullTime = {job.id, pay, benefits, schedule}
partTime = {job.id, wage, schedule}
contract = {job.id, terms, pay, schedule}
certs = {name, cert_body, cost, requirements}
jobCerts = {job.id, cert.id}
jobRole = {title, avgWage, description} """

#tables = {"certification", "company", "contact", "contract", "full_time", "job", "job_certs", "job_role", "part_time"}

tables = {}

def getTables():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("SHOW TABLES")
    myResult = myCursor.fethone()
    while myResult is not None:
        tables.append(myResult)
        myReslut = myCursor.fetchone()
    connection.close()

def showTables():
    number=1
    for table in tables:
        print(f"{number} {table}")
        number=number+1




menuText = """Please select one of the following options:
1) Display Tables
2) Add a company
3) Update a company
4) Delete a company
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            showTables()
        elif menuOption == "2":
            addCompany()
        elif menuOption == "3":
            updateCompany()
        elif menuOption == "4":
            deleteCompany()
