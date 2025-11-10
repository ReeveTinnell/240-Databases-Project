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
    myCursor.execute(f"DESCRIBE {table}")
    attributes = myCursor.fetchall()
    # for row in attributes:
    #     print(row)
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
    number=0
    tables = []
    tables = getTables()
    for table in tables:
        print(f"{number}. {table}")
        number=number+1
    print("\n")

def showTable(table):

    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute(f"SELECT * FROM {table}")
    results = myCursor.fetchall()
    print(f"\nIn the {table} table, we have the following items: ")
    for row in results:
        print(row)

    connection.close()
    print("\n")

def addTo():

    connection = getConnection()
    myCursor = connection.cursor()

    showAll()
    table = int(input("\n Please enter the number of a table you would like to add to: "))
    table = selectTable(table)

    #grabs the attributes for the selected table
    attributes = getAttributes(table)

    #blank lists to generate the strings necesaary for SQL. Using two different lists, might be able to use something more sophisticated, but this works
    entryValues = []
    entryAttr = []

    #grabs user input for each attribute and maps it to the same order as attributes.
    for row in attributes:
        if row[0] == "id":
            continue
        else:
            value = input(f"Please enter the value for {table} value {row[0]}: ")
            entryValues.append(value)
            entryAttr.append(row[0])

    #string construction for query statement
    entryString = ', '.join(['%s'] * len(entryValues))
    entryAttr = ', '.join(entryAttr)
    query = f"INSERT INTO {table} ({entryAttr}) VALUES ({entryString})"

    myCursor.execute(query, entryValues)
    connection.commit()
    print("\nYour entry was successfully Added!\n")
    connection.close()

def delFrom():
    # Takes user input to select a table from the database
    connection = getConnection()
    myCursor = connection.cursor()

    showAll()
    table = int(input("\n Please enter the number of a table you would like make a deletion from: "))
    table = selectTable(table)
    showTable(table)
    deleteRow = int(input("\n Please enter the id of the entry you would like to delete: \n"))
    myCursor.execute(f"DELETE FROM {table} WHERE id={deleteRow}")
    connection.commit()
    print("\nYour entry was successfully deleted!")
    connection.close()

def selectTable(table):
    tables = getTables()
    table = tables[table]
    return table


def updateEntry(table, entry):

    attributes = getAttributes(table)

    entryValues = []
    entryAttr = []

    for row in attributes:
       if row[0] == "id":
           print(f"You are modifying entry id # {entry} in the {table} Table. Proceed with caution")
           continue
       else:
           value = input(f"Please enter the new value for {table} {entry} value {row[0]}: ")
           entryValues.append(value)
           entryAttr.append(row[0])

    # Construct update Query string
    queryString = []
    index = 0
    for column in entryValues:
        queryString.append(f"{entryAttr[index]} = %s")
        index = index + 1
    queryString = ', '.join(queryString)
    print(queryString)
    query = f"UPDATE {table} SET {queryString} WHERE id={entry}"
    print(query)
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute(query, entryValues)
    connection.commit()
    connection.close()


menuText = """Please select one of the following options:
1) Show All Tables
2) Show Contents of any Table
3) Add to a table
4) Update a table (in testing)
5) Delete a table entry
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            showAll()
        elif menuOption == "2":
            showAll()
            tables = getTables()
            table = int(input("\nSelect a table to view: \n"))
            table = tables[table]
            showTable(table)
        elif menuOption == "3":
            addTo()
        elif menuOption == "4":
            showAll()
            tables = getTables()
            table = int(input("\nSelect a table you wish to update:  \n"))
            table = tables[table]
            showTable(table)
            entry = int(input("\nSelect the entry id you wish to update: \n"))
            updateEntry(table, entry)
        elif menuOption == "5":
            delFrom()

