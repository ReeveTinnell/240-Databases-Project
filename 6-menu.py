#!/usr/bin/env python3
# This example uses a credentials stored in a .env file defining SQL_HOST, SQL_USER, SQL_PWD, and SQL_DB

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

def printTable():
    table = selectTable()
    connection = getConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM " + table)
    myresult = mycursor.fetchone()
    print("In the " + table + " table, we have the following items: ")
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
    industry = input ("Companies industry")
    connection = getConnection()
    mycursor = connection.cursor()
    query = "INSERT INTO company (name, industry, location, size, website) values (%s, %s, %s, %s, %s);"
    mycursor.execute(query, (name, industry, location, size, website))
    connection.commit()
    connection.close()

def deleteCompany():
    rowToDelete = input("What is the id of the row to delete? ")
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("delete from actor where actor_id=%s", (rowToDelete,))
    connection.commit()
    connection.close()

def updateCompany():
    rowToUpdate = input("What is the id of the row you want to update? ")
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select * from actor where actor_id=%s", (rowToUpdate,))
    myResult = myCursor.fetchone()
    print(f"The current row has the value: {myResult}")
    firstname = input("Please give the first name of the actor: ")
    lastname = input("Please give the last name of the actor: ")
    myCursor.execute("update actor set first_name=%s, last_name=%s where actor_id=%s", (firstname, lastname, rowToUpdate))
    connection.commit()
    connection.close()

def selectTable():
    tableOption = "1"
    while tableOption != 'q':
        tableOption = input(tableText)
        if tableOption == "1":
            return "company"
        elif tableOption == "2":
            return "contact"
        elif tableOption == "3":
            return "job"
        elif tableOption == "4":
            return "full_time"
        elif tableOption == "5":
            return "part_time"
        elif tableOption == "6":
            return "contract"
        elif tableOption == "7":
            return "job_certs"
        elif tableOption == "8":
            return "certification"
        elif tableOption == "9":
            return "job_role"

menuText = """Please select one of the following options:
1) Display contents of table
2) Add a company
3) Update a company
4) Delete a company
q) Quit
"""

tableText = """Please select from the following tables:
1) Company
2) Contact
3) Job
4) Full_Time
5) Part_Time
6) Contract
7) Job_Certs
8) Certification
9) Job_Role
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            printTable()
        elif menuOption == "2":
            addCompany()
        elif menuOption == "3":
            updateCompany()
        elif menuOption == "4":
            deleteCompany()

