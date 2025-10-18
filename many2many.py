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

def printJobs():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select * from job")
    myResult = myCursor.fetchone()
    print("In the job table, we have the following items: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()

def printCerts():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select * from certification")
    myResult = myCursor.fetchone()
    print("In the certification table, we have the following items: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()

def printCertsForJob():
    connection = getConnection()
    myCursor = connection.cursor()
    job_id = input("For which job_id would you like to view the certifications? #> ")
    myCursor.execute("SELECT certification.id, job.title, certification.name FROM job_certs JOIN job ON job_certs.job_id=job.id JOIN certification ON job_certs.cert_id=certification.id WHERE job_id=%s", (job_id,))
    myResult = myCursor.fetchall()
    print(f"There are {len(myResult)} certifications: ")
    for row in myResult:
        print(row)
    print()

def printJobsWithCert():
    connection = getConnection()
    myCursor = connection.cursor()
    cert_id = input("For which cert_id would you like to view the jobs? #> ")
    myCursor.execute("SELECT job.id, job.title, certification.name FROM job_certs JOIN job ON job_certs.job_id=job.id JOIN certification ON job_certs.cert_id=certification.id WHERE cert_id=%s", (cert_id,))
    myResult = myCursor.fetchall()
    print(f"There are {len(myResult)} jobs: ")
    for row in myResult:
        print(row)
    print()

def addCert():
    printJobs()
    print(" ")
    printCerts()
    print(" ")
    connection = getConnection()
    myCursor = connection.cursor()
    addToJob = input("Please provide the job.id you would like to add a certification to #> ")
    addCert = input("What certification (cert.id) would you like to add to this job? #> ")
    query = "INSERT INTO job_certs (job_id, cert_id) VALUES (%s, %s)"
    myCursor.execute(query, (addToJob, addCert))
    connection.commit()
    connection.close()

    
def removeCert():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT job.id, job.title, certificate.id, certification.name FROM job_certs JOIN job ON job_certs.job_id=job.id JOIN certification ON job_certs.cert_id=certification.id")
    jobCerts = myCursor.fetchall()
    print(f"There are {len(jobCerts)} certifications required for jobs in the database:")
    for cert in jobCerts:
        print(cert)
    print()


menuText = """Please select one of the following options:
1) Print jobs
2) Print certifications
3) Print certifications for a job
4) Print jobs which require a certification
5) Add a certification to a job (unimplemented)
6) Remove a certification from a job (unimplemented)
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            printJobs()
        elif menuOption == "2":
            printCerts()
        elif menuOption == "3":
            printCertsForJob()
        elif menuOption == "4":
            printJobsWithCert()
        elif menuOption == "5":
            addCert()
        elif menuOption == "6":
            removeCert()