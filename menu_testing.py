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


"""
getAttributes fuction takes a table and returns the attributes (columns) of a table. 
"""
def getAttributes(table):
    attributes = []
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("DESCRIBE %s", (table))
    myResult = myCursor.fetchone()
    while myResult is not None:
        myResult = ' '.join(myResult)
        myResult = myResult.strip()
        attributes.append(myResult)
        myResult = myCursor.fetchone()
    return attributes
    connection.close()


def getTables():
    tables = []
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("SHOW TABLES")
    myResult = myCursor.fetchone()
    while myResult is not None:
        myResult = ' '.join(myResult)
        myResult = myResult.strip()
        tables.append(myResult)
        myResult = myCursor.fetchone()
    return tables
    connection.close()

def showAll():
    number=1
    tables = []
    tables = getTables()
    for table in tables:
        print(f"{number}. {table}")
        number=number+1
    print("")

def showTable():
    showAll()
    tableSelection = input("Select a table to view")
    tables = getTables()
    tableOption = tables[tableSelection - 1] 
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT * FROM %s", (tableOption))
    myResult = myCursor.fetchone()
    print(f"In the {tableOption} table, we have the following items: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()


menuText = """Please select one of the following options:
1) Show All Tables
2) Show Contents of a Table
3) Add a company
4) Update a company
5) Delete a company
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            showAll()
        elif menuOption == "2":
            showTable()
        elif menuOption == "3":
            updateCompany()
        elif menuOption == "4":
            deleteCompany()
