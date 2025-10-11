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

def showCompanies():
    connection = getConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM company")
    myresult = mycursor.fetchone()
    print("In the company table, we have the following items: ")
    while myresult is not None:
        print(myresult)
        myresult = mycursor.fetchone()
    connection.close()
    print()

def addCompany():
    name = input("Company name: ")
    website = input("Company website: ")
    size = input ("Company size: ")
    location = input ("Company location: ")
    industry = input ("Companies industry: ")
    connection = getConnection()
    myCursor = connection.cursor()
    query = "INSERT INTO company (name, industry, location, size, website) values (%s, %s, %s, %s, %s);"
    myCursor.execute(query, (name, industry, location, size, website))
    connection.commit()
    connection.close()

def deleteCompany():
    rowToDelete = input("What is the id of the company you wish to delete? ")
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("DELETE FROM company where id=%s", (rowToDelete,))
    connection.commit()
    connection.close()

def updateCompany():
    rowToUpdate = input("What is the id of the row you want to update? ")
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select * from company where id=%s", (rowToUpdate,))
    myResult = myCursor.fetchone()
    print(f"The current row has the value: {myResult}")
    name = input("Company name: ")
    website = input("Company website: ")
    size = input ("Company size: ")
    location = input ("Company location: ")
    industry = input ("Companies industry: ")
    query = "INSERT INTO company (name, industry, location, size, website) values (%s, %s, %s, %s, %s);"
    myCursor.execute(query, (name, industry, location, size, website))
    connection.commit()
    connection.close()


menuText = """Please select one of the following options:
1) Display companies
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
            showCompanies()
        elif menuOption == "2":
            addCompany()
        elif menuOption == "3":
            updateCompany()
        elif menuOption == "4":
            deleteCompany()

