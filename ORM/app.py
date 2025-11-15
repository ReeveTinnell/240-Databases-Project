#! /usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from models import *
from sqlalchemy.orm import joinedload

app = Flask(__name__) # creates a flask application object

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

# example database uri = "mysql+pymysql://jeff:mypass@localhost/sakila"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}/{creds['db']}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = creds['secret_key']

db.init_app(app)

def showCompanies():
    print("\n")
    companies = Company.query.all()
    for company in companies:
        print(f"[{company.id}] -> {company.name}")
    print("\n")

@app.route('/')
def home():
    tables = db.metadata.tables.keys()
    print(tables)
    return(render_template('home.html'))

@app.route('/about')
def about():
    return(render_template('about.html'))

# @app.route('/viewTable', methods=['GET'])
# def viewTable():
#     output = render_template('viewTable.html', table=table, attributes=attributes)
#     return output

#               JOBS
@app.route('/jobs')
def jobs():
    jobs = Job.query.options(
        joinedload(Job.ft),
        joinedload(Job.pt),
        joinedload(Job.contract),
        joinedload(Job.certs)
        ).all()

    for job in jobs:
        print(job.company.name)
    return(render_template('jobs.html', jobs=jobs))

@app.route('/job/<int:id>', methods=['GET'])
def job(id):
    job = Job.query.get(id)
    return(render_template('job.html', job=job))


#               CERTIFICATIONS

@app.route('/addCert')
def addCertForm():
    return(render_template('addCert.html'))

@app.route('/addCert', methods=['POST'])
def addCert():
    new_cert = Cert(name=request.form['name'], cert_body=request.form['cert_body'], cost=request.form['cost'], requirements=request.form['requirements'], link=request.form['link'])
    db.session.add(new_cert)
    db.session.commit()
    return redirect(url_for('viewCerts'))

@app.route('/viewCerts')
def viewCerts():
    certs = Cert.query.all()
    return(render_template('viewCerts.html', certs=certs))

@app.route('/cert/<int:id>', methods=['GET'])
def cert(id):
    cert = Cert.query.get(id)
    return(render_template('cert.html', cert=cert))


@app.route('/addJobCertForm/<int:id>')
def addJobCertForm(id):
    job = Job.query.get(id)
    certs = Cert.query.all()
    return(render_template('addJobCertForm.html', job=job, certs=certs))

@app.route('/addJobCert/<int:job>/<int:cert>', methods=['GET'])
def addJobCert(job, cert):
    new_job_cert = JobCert(job=job, cert=cert)
    db.session.add(new_job_cert)
    db.session.commit()
    job = Job.query.get(job)
    return(render_template('job.html', job=job))

@app.route('/delJobCert/<int:job>/<int:cert>', methods=['GET'])
def defJobCert(job, cert):

    del_job_cert = JobCert.query.filter_by(job=job, cert=cert).first()

    print(del_job_cert)

    db.session.delete(del_job_cert)
    db.session.commit()
    return redirect(f'/job/{job}')


@app.route('/deleteCert/<int:id>')
def deleteCert(id):
    output = render_template('deleteCert.html', id=id)
    return output


@app.route('/deleteCert', methods=['POST'])
def deleteCertFromTable():

    id = request.form['id']
    name = request.form['name']

    error = None

    cert = db.session.get(Cert, id)

    if cert.name != name:
        flash('Certification name does not match. Deletion cancelled.', 'error')
        return redirect(f'/deleteCert/{id}')
    else:
        db.session.delete(cert)
        db.session.commit()
        return redirect(url_for('viewCerts'))


#               COMPANIES
@app.route('/companies')
def viewCompanies():
    companies = Company.query.all()
    output = render_template('viewCompanies.html', companies=companies)
    return output

@app.route('/addCompany')
def addCompany():
    output = render_template('addCompany.html')
    return output

@app.route('/addCompany', methods=['POST'])
def addCompanyToList():

    new_company = Company(name=request.form['name'], industry=request.form['industry'], location=request.form['location'], size=request.form['size'], website=request.form['website'])
    db.session.add(new_company)
    db.session.commit()

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

    company = db.session.get(Company, id)

    if company == None:
        error="ERROR! No company found, please enter a correct company id"
        output = render_template('deleteCompany.html', error=error)
        return output
    if company.name != name:
        error="ERROR! Company name does not match company name file"
        output = render_template('deleteCompany.html', error=error)
        return output
    else:
        db.session.delete(company)
        db.session.commit()
        return redirect(url_for('viewCompanies'))

@app.route('/updateCompany')
def updateCompany():
    company = Company.query.get(request.args.get("id"))
    output = render_template('updateCompanyForm.html', company=company)
    return output


@app.route('/updateCompany', methods=['POST'])
def updateCompanyEntry():

    id = request.form['id']
    
    company = db.session.get(Company, id)

    company.name = request.form['name'],
    company.industry = request.form['industry'],
    company.location = request.form['location'],
    company.size = request.form['size'],
    company.website = request.form['website']

    db.session.commit()

    return redirect(url_for('viewCompanies'))


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")


