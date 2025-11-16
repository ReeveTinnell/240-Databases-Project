#! /usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

#               COMPANIES

#   CREATE

@app.route('/api/company', methods=['POST'])
def create_company():
    data = request.json
    new_company = Company(
        name=data['name'],
        industry=data.get('industry'),
        location=data.get('location'),
        size=data.get('size'),
        website=data.get('website')
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'id': new_company.id, 'name': new_company.name})

#   READ

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


#   CREATE - vibe coded

@app.route('/job/new', methods=['GET', 'POST'])
def newJob():
    if request.method == 'POST':
        # Get job data
        job_data = {
            'title': request.form['title'],
            'post_date': datetime.strptime(request.form['post_date'], '%Y-%m-%d') if request.form.get('post_date') else None,
            'close_date': datetime.strptime(request.form['close_date'], '%Y-%m-%d') if request.form.get('close_date') else None,
            'hyperlink': request.form.get('hyperlink'),
            'company_id': int(request.form['company_id']),
            'role_id': int(request.form['role_id']) if request.form.get('role_id') else None,
            'contact_id': int(request.form['contact_id']) if request.form.get('contact_id') else None
        }

        # Create job
        new_job = Job(**job_data)
        db.session.add(new_job)
        db.session.flush()  # Get the job.id before committing

        # Handle job type (ft, pt, or contract)
        job_type = request.form['job_type']
        if job_type == 'full_time':
            ft = Ft(
                id=new_job.id,
                hourly=request.form.get('ft_hourly'),
                schedule=request.form.get('ft_schedule'),
                benefits=request.form.get('benefits')
            )
            db.session.add(ft)
        elif job_type == 'part_time':
            pt = Pt(
                id=new_job.id,
                hourly=request.form.get('pt_hourly'),
                schedule=request.form.get('pt_schedule'),
                weeklyHours=request.form.get('weeklyHours')
            )
            db.session.add(pt)
        elif job_type == 'contract':
            contract = Contract(
                id=new_job.id,
                terms=request.form.get('terms'),
                schedule=request.form.get('contract_schedule'),
                pay=request.form.get('pay')
            )
            db.session.add(contract)

        # Handle certifications (many-to-many)
        cert_ids = request.form.getlist('cert_ids')
        for cert_id in cert_ids:
            if cert_id:
                job_cert = JobCert(job=new_job.id, cert=int(cert_id))
                db.session.add(job_cert)

        db.session.commit()
        return redirect(url_for('job', id=new_job.id))

    # GET request - show form
    companies = Company.query.all()
    roles = Role.query.all()
    contacts = Contact.query.all()
    certs = Cert.query.all()

    return(render_template('addJob.html',
                         companies=companies,
                         roles=roles,
                         contacts=contacts,
                         certs=certs))

#   READ
@app.route('/job/all')
def jobs():
    jobs = Job.query.options(
        joinedload(Job.ft),
        joinedload(Job.pt),
        joinedload(Job.contract),
        joinedload(Job.certs)
        ).all()
    return(render_template('jobs.html', jobs=jobs))

@app.route('/job/<int:id>', methods=['GET'])
def job(id):
    job = Job.query.get(id)
    return(render_template('job.html', job=job))

#   UPDATE
@app.route('/job/update/<int:id>', methods =['GET'])
def updateJobForm(id):

    job = Job.query.get(id)
    return(render_template('updateJob.html', job=job))

#   DELETE
@app.route('/job/delete/<int:id>', methods=['GET'])
def deleteJobForm(id):
    job = Job.query.get(id)
    return(render_template('deleteJob.html', job=job))

@app.route('/job/delete/<int:id>', methods=['POST'])
def deleteJobFromTable(id):
    job = Job.query.get(id)
    for cert in job.certs:
        del_job_cert = JobCert.query.filter_by(job=id, cert=cert.id).first()
        db.session.delete(del_job_cert)
        db.session.commit()
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('jobs'))


#               CERTIFICATIONS
#   CREATE
@app.route('/cert/new')
def addCertForm():
    return(render_template('addCert.html'))

@app.route('/cert/new', methods=['POST'])
def addCert():
    new_cert = Cert(name=request.form['name'], cert_body=request.form['cert_body'], cost=request.form['cost'], requirements=request.form['requirements'], link=request.form['link'])
    db.session.add(new_cert)
    db.session.commit()
    return redirect(url_for('viewCerts'))

#   CREATE endpoint for 'newJob'
@app.route('/api/cert', methods=['POST'])
def create_cert():
    data = request.json
    new_cert = Cert(
        name=data['name'],
        cert_body=data['cert_body'],
        cost=data.get('cost'),
        requirements=data.get('requirements'),
        link=data.get('link')
    )
    db.session.add(new_cert)
    db.session.commit()
    return jsonify({'id': new_cert.id, 'name': new_cert.name})

#   READ
@app.route('/cert/all')
def viewCerts():
    certs = Cert.query.all()
    return(render_template('viewCerts.html', certs=certs))

@app.route('/cert/<int:id>', methods=['GET'])
def cert(id):
    cert = Cert.query.get(id)
    return(render_template('cert.html', cert=cert))

#   UPDATE
@app.route('/cert/update/<int:id>', methods=['GET'])
def updateCertForm(id):
    cert = Cert.query.get(id)
    return(render_template('updateCert.html', cert=cert))

@app.route('/cert/update/<int:id>', methods=['POST'])
def updateCert(id):
    cert = Cert.query.get(id)

    cert.name = request.form['name']
    cert.cert_body = request.form['cert_body']
    cert.cost = request.form['cost']
    cert.requirements = request.form['requirements']
    cert.link = request.form['link']

    db.session.commit()

    return redirect(url_for('viewCerts'))


#   DELETE
@app.route('/cert/delete/<int:id>')
def deleteCert(id):
    output = render_template('deleteCert.html', id=id)
    return output

@app.route('/cert/delete/<int:id>', methods=['POST'])
def deleteCertFromTable(id):

    name = request.form['name']

    error = None

    cert = Cert.query.get(id)

    if cert.name != name:
        flash('Certification name does not match. Deletion cancelled.', 'error')
        return redirect(f'/deleteCert/{id}')
    else:
        db.session.delete(cert)
        db.session.commit()
        return redirect(url_for('viewCerts'))

#             JOB_CERTS

#   Create
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

#   READ
@app.route('/job_certs')
def viewJobCerts():
    job_certs = JobCert.query.all()
    return(render_template('viewJobCerts.html', job_certs=job_certs))

#   DELETE
@app.route('/delJobCert/<int:job>/<int:cert>', methods=['GET'])
def defJobCert(job, cert):

    del_job_cert = JobCert.query.filter_by(job=job, cert=cert).first()


    db.session.delete(del_job_cert)
    db.session.commit()
    return redirect(f'/job/{job}')



#               COMPANIES

#   READ
@app.route('/companies')
def viewCompanies():
    companies = Company.query.all()
    output = render_template('viewCompanies.html', companies=companies)
    return output

#   CREATE
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

#               CONTACTS
#   CREATE

@app.route('/api/contact', methods=['POST'])
def create_contact():
    data = request.json
    new_contact = Contact(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        position=data.get('position'),
        company=int(data['company_id'])
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'id': new_contact.id, 'name': new_contact.name})


#               ROLES
#   CREATE
@app.route('/api/role', methods=['POST'])
def create_role():
    data = request.json
    new_role = Role(
        title=data['title'],
        avg_wage=data.get('avg_wage'),
        description=data.get('description')
    )
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'id': new_role.id, 'title': new_role.title})



if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")


