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



@app.route('/')
def home():
    tables = db.metadata.tables.keys()
    print(tables)
    return(render_template('home.html', tables=tables))

@app.route('/about')
def about():
    return(render_template('about.html'))

#               JOBS


#   CREATE
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
    job = Job.query.options(
        joinedload(Job.ft),
        joinedload(Job.pt),
        joinedload(Job.contract),
        joinedload(Job.certs)
        ).get(id)
    companies = Company.query.all()
    roles = Role.query.all()
    contacts = Contact.query.all()
    certs = Cert.query.all()
    return(render_template('updateJob.html', job=job, companies=companies, roles=roles, contacts=contacts, certs=certs))


@app.route('/job/update/<int:id>', methods =['POST'])
def updateJob(id):
    job = Job.query.options(
        joinedload(Job.ft),
        joinedload(Job.pt),
        joinedload(Job.contract),
        joinedload(Job.certs)
        ).get(id)
        
    if job.ft:
        oldType = 'full_time'
    elif job.pt:
        oldType = 'part_time'
    elif job.contract:
        oldType = 'contract'
        
    job.title = request.form['title'],
    job.post_date = datetime.strptime(request.form['post_date'], '%Y-%m-%d') if request.form.get('post_date') else None,
    job.close_date = datetime.strptime(request.form['close_date'], '%Y-%m-%d') if request.form.get('close_date') else None,
    job.hyperlink = request.form.get('hyperlink'),
    job.company_id = int(request.form['company_id']),
    job.role_id = int(request.form['role_id']) if request.form.get('role_id') else None,
    job.contact_id = int(request.form['contact_id']) if request.form.get('contact_id') else None    

    job_type = request.form['job_type']

    if job_type == oldType:
        if job_type == 'full_time':
            ft = Ft.query.get(id)
            ft.hourly = request.form.get('ft_hourly'),
            ft.schedule = request.form.get('ft_schedule'),
            ft.benefits = request.form.get('ft_benefits')
        elif job_type == 'part_time':
            pt = Pt.query.get(id)
            pt.hourly = request.form.get('pt_hourly'),
            schedule = request.form.get('pt_schedule'),
            weeklyHours = request.form.get('weeklyHours')
        elif job_type == 'contract':
            contract = Contract.query.get(id)
            contract.terms = request.form.get('terms'),
            contract.schedule = request.form.get('contract_schedule'),
            contract.pay = request.form.get('pay')
    elif job_type != oldType:
        if oldType.ft:
            ft = Ft.query.get(id)
            db.session.delete(ft)
        elif oldType.pt:
            pt = Pt.query.get(id)
            db.session.delete(pt)
        elif oldType.conract:
            contract = Contract.query.get(id)
            db.session.delete(contract)

    
    # Handle certifications (many-to-many)
    updateCertIds = request.form.getlist('cert_ids')
    
    updateCertIds = [int(cert_id) for cert_id in updateCertIds if cert_id]
   
    # Delete any certifcations that are no longer required
    for cert in job.certs:
        if cert.id not in updateCertIds:
            delJobCert = JobCert.query.filter_by(job=id, cert=cert.id).first()
            db.session.delete(delJobCert)
    
    for cert_id in updateCertIds:
        if not JobCert.query.filter_by(job=id, cert=cert_id).first():
            newJobCert = JobCert(job=id, cert=cert_id)
            db.session.add(newJobCert)
    
    db.session.commit()
    return redirect(url_for('job', id=id))


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
@app.route('/job_cert/add/<int:id>')
def addJobCertForm(id):
    job = Job.query.get(id)
    certs = Cert.query.all()
    return(render_template('addJobCertForm.html', job=job, certs=certs))

@app.route('/job_cert/add/<int:job>/<int:cert>', methods=['GET'])
def addJobCert(job, cert):
    new_job_cert = JobCert(job=job, cert=cert)
    db.session.add(new_job_cert)
    db.session.commit()
    job = Job.query.get(job)
    return(render_template('job.html', job=job))

#   READ
@app.route('/job_cert/all')
def viewJobCerts():
    job_certs = JobCert.query.all()
    return(render_template('viewJobCerts.html', job_certs=job_certs))

#   DELETE
@app.route('/job_cert/delete/<int:job>/<int:cert>', methods=['GET'])
def defJobCert(job, cert):

    del_job_cert = JobCert.query.filter_by(job=job, cert=cert).first()


    db.session.delete(del_job_cert)
    db.session.commit()
    return redirect(f'/job/{job}')



#               COMPANIES

#   CREATE

@app.route('/api/company', methods=['POST'])
def create_company():
    data = request.json
    newCompany = Company(
        name=data['name'],
        industry=data.get('industry'),
        location=data.get('location'),
        size=data.get('size'),
        website=data.get('website')
    )
    db.session.add(newCompany)
    db.session.commit()
    return jsonify({'id': newCompany.id, 'name': newCompany.name})

#   READ
@app.route('/company/all')
def viewCompanies():
    companies = Company.query.all()
    output = render_template('viewCompanies.html', companies=companies)
    return output

#   CREATE
@app.route('/company/new')
def addCompany():
    output = render_template('addCompany.html')
    return output

@app.route('/company/new', methods=['POST'])
def addCompanyToList():

    new_company = Company(name=request.form['name'], industry=request.form['industry'], location=request.form['location'], size=request.form['size'], website=request.form['website'])
    db.session.add(new_company)
    db.session.commit()

    return redirect(url_for('viewCompanies'))

@app.route('/company/delete/<int:company>', methods=['GET'])
def deleteCompany(company):
    company = Company.query.get(company)
    print(company)
    return(render_template('deleteCompany.html', company=company))
    
@app.route('/company/delete/<int:company>', methods=['POST'])
def deleteCompanyFromTable(company):

    company = Company.query.get(company)
    
    name = request.form['name']

    error = None

    if company.name != name:
        error="ERROR! Company name does not match company name file"
        output = render_template('deleteCompany.html', error=error)
        return output
    else:
        db.session.delete(company)
        db.session.commit()
        return redirect(url_for('viewCompanies'))

@app.route('/company/update/<int:company>')
def updateCompany(company):
    company = Company.query.get(company)
    output = render_template('updateCompanyForm.html', company=company)
    return output


@app.route('/company/update/<int:company>', methods=['POST'])
def updateCompanyEntry(company):
    
    company = Company.query.get(company)

    company.name = request.form['name'],
    company.industry = request.form['industry'],
    company.location = request.form['location'],
    company.size = request.form['size'],
    company.website = request.form['website']

    db.session.commit()

    return redirect(url_for('viewCompanies'))

#               CONTACTS
#   CREATE

@app.route('/contact/all')
def viewContacts():
    contacts = Contact.query.all()
    return(render_template('viewContacts.html', contacts=contacts))

@app.route('/contact/new')
def newContactForm():
    companies = Company.query.all()
    return(render_template('addContact.html', companies=companies))

@app.route('/contact/new', methods=['POST'])
def newContact():
    newContact = Contact(
        name=request.form['name'],
        email=request.form['email'],
        phone=request.form['phone'],
        position=request.form['position'],
        company_id=int(request.form['company_id'])
    )
    db.session.add(newContact)
    db.session.commit()
    return redirect(url_for('viewContacts'))

@app.route('/contact/delete/<int:id>', methods=['GET'])
def deleteContactdForm(id):
    contact = Contact.query.get(id)
    return(render_template('deleteContact.html', contact=contact))

@app.route('/contact/delete/<int:id>', methods=['POST'])
def deleteContact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('viewContacts'))
    
@app.route('/api/contact', methods=['POST'])
def newContactAPI():
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

@app.route('/contact/update/<int:id>')
def updateContactForm(id):
    contact = Contact.query.get(id)
    companies = Company.query.all()
    return(render_template('updateContactForm.html', contact=contact, companies=companies))

@app.route('/contact/update/<int:id>', methods=['POST'])
def updateContact(id):
    contact = Contact.query.get(id)
    
    contact.company_id = request.form['company_id']
    contact.name = request.form['name']
    contact.email = request.form['email']
    contact.phone = request.form['phone']
    contact.position = request.form['position']
    
    db.session.commit()
    
    return redirect(url_for('viewContacts'))


@app.route('/contract/all')
def viewContracts():
    contracts = Contract.query.all()
    return(render_template('viewContracts.html', contracts=contracts))
    
@app.route('/full_time/all')
def viewFt():
    ftJobs = Ft.query.all()
    return(render_template('viewFt.html', ftJobs=ftJobs))

@app.route('/part_time/all')
def viewPt():
    ptJobs = Pt.query.all()
    return(render_template('viewPt.html', ptJobs=ptJobs))

#               ROLES
#   CREATE
@app.route('/api/role', methods=['POST'])
def createRole():
    data = request.json
    newRole = Role(
        title=data['title'],
        avg_wage=data.get('avg_wage'),
        description=data.get('description')
    )
    db.session.add(newRole)
    db.session.commit()
    return jsonify({'id': newRole.id, 'title': newRole.title})

@app.route('/role/all')
def viewRoles():
    roles = Role.query.all()
    return(render_template('viewRoles.html', roles=roles))
    
@app.route('/role/new')
def newRoleForm():
    return(render_template('addRole.html'))
    
@app.route('/role/new', methods=['POST'])
def newRole():
    
    newRole = Role(title=request.form['name'], avg_wage=reqest.form['avg_wage'], description=request.form['description'])
    db.session.add(newRole)
    db.sesssion.commit()
    
    return redirect(url_for('viewRoles'))


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")


