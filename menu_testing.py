#!/usr/bin/env python3

#import mysql.connector, os

""" company = {name, industry, website, location, size}
contact = {name, email, phone, position}
job = {title, post_date, close_date, hyperlink}
fullTime = {job.id, pay, benefits, schedule}
partTime = {job.id, wage, schedule}
contract = {job.id, terms, pay, schedule}
certs = {name, cert_body, cost, requirements}
jobCerts = {job.id, cert.id}
jobRole = {title, avgWage, description} """

tables = {"certification", "company", "contact", "contract", "full_time", "job", "job_certs", "job_role", "part_time"}

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
