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

def getTable(table):

    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute(f"SELECT * FROM {table}")
    results = myCursor.fetchall()
    connection.close()

    return results

def getEntry(table, id):
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute(f"SELECT * FROM {table} WHERE id={id}")
    results = myCursor.fetchall()
    connection.close()
    print(results)
    return results


def addTo(table, entryValues):

    connection = getConnection()
    myCursor = connection.cursor()

    #grabs the attributes for the selected table
    attributes = getAttributes(table)

    #blank lists to generate the strings necesaary for SQL. Using two different lists, might be able to use something more sophisticated, but this works
    entryAttr = []

    #grabs user input for each attribute and maps it to the same order as attributes.
    for row in attributes:
        if row[0] == "id":
            continue
        else:
            entryAttr.append(row[0])

    #string construction for query statement
    entryString = ', '.join(['%s'] * len(entryValues))
    entryAttr = ', '.join(entryAttr)
    query = f"INSERT INTO {table} ({entryAttr}) VALUES ({entryString})"

    myCursor.execute(query, entryValues)
    connection.commit()
    print("\nYour entry was successfully Added!\n")
    connection.close()

def delFrom(table, deletion):

    connection = getConnection()
    myCursor = connection.cursor()

    myCursor.execute(f"DELETE FROM {table} WHERE id={deletion}")
    connection.commit()
    connection.close()

def selectTable(table):
    tables = getTables()
    table = tables[table]
    return table


def updateEntry(table, id, updateValues):

    connection = getConnection()
    myCursor = connection.cursor()

    #grabs the attributes for the selected table
    attributes = getAttributes(table)

    #blank lists to generate the strings necesaary for SQL. Using two different lists, might be able to use something more sophisticated, but this works
    entryAttr = []

    #grabs user input for each attribute and maps it to the same order as attributes.
    for row in attributes:
        if row[0] == "id":
            continue
        else:
            entryAttr.append(row[0])

    print(f"The entyrAttr is: {entryAttr}")

    #string construction for query statement
    entryString = ', '.join(['%s'] * len(updateValues))

    # Construct update Query string
    queryString = []
    index = 0
    for column in updateValues:
        queryString.append(f"{entryAttr[index]} = %s")
        index = index + 1
    queryString = ', '.join(queryString)
    print(queryString)
    query = f"UPDATE {table} SET {queryString} WHERE id={id}"
    print(query)
    myCursor.execute(query, updateValues)
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

