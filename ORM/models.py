from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cert(db.Model):
    # Connecting class to database table name
    __tablename__ = 'cert'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    cert_body = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Numeric(6,2), nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)

    jobs = db.relationship('Job', secondary='job_cert', viewonly='true')



class Company(db.Model):
    # Connecting class to database table name
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    industry = db.Column(db.String(20), nullable=True)
    location = db.Column(db.Text, nullable=True)
    size = db.Column(db.String(10), nullable=True)
    website = db.Column(db.Text, nullable=True)
    
class Contact(db.Model):
    # Connecting class to database table name
    __tablename__ = 'contact'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    phone = db.Column(db.String(14), unique=True, nullable=True)
    name = db.Column(db.Text, nullable=True)
    position = db.Column(db.Text, nullable=True)
    company = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    
class Contract(db.Model):
    # Connecting class to database table name
    __tablename__ = 'contract'

    id = db.Column(db.Integer, db.ForeignKey("job.id", ondelete='CASCADE'), primary_key=True, autoincrement=True)
    terms =  db.Column(db.Text, nullable=True)
    schedule =  db.Column(db.Text, nullable=True)
    pay =  db.Column(db.Text, nullable=True)
    
class Ft(db.Model):
    # Connecting class to database table name
    __tablename__ = 'full_time'
    
    id = db.Column(db.Integer, db.ForeignKey("job.id", ondelete='CASCADE'), primary_key=True, autoincrement=True)
    hourly =  db.Column(db.Numeric(4,2), nullable=True)
    schedule =  db.Column(db.Text, nullable=True)
    benefits =  db.Column(db.Text, nullable=True)
    
class Pt(db.Model):
    # Connecting class to database table name
    __tablename__ = 'part_time'

    id = db.Column(db.Integer, db.ForeignKey("job.id", ondelete='CASCADE'), primary_key=True, autoincrement=True)
    hourly =  db.Column(db.Numeric(4, 2), nullable=True)
    schedule =  db.Column(db.Text, nullable=True)
    weeklyHours = db.Column(db.Integer, nullable=True)

class Job(db.Model):
    # Connecting class to database table name
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.Date, nullable=True)
    close_date = db.Column(db.Date, nullable=True)
    hyperlink = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=True)

    # Relationships
    company = db.relationship('Company', backref='job')
    role = db.relationship('Role', backref='job')
    contact = db.relationship('Contact', backref='job')

    # Subtypes

    ft = db.relationship('Ft', backref='job', uselist=False, cascade='all, delete-orphan')
    pt = db.relationship('Pt', backref='job', uselist=False, cascade='all, delete-orphan')
    contract = db.relationship('Contract', backref='job', uselist=False, cascade='all, delete-orphan')

    @property
    def type(self):
        """Returns the job type details"""
        if self.ft:
            return("Full Time")
        elif self.pt:
            return("Part Time")
        elif self.contract:
            return("Contract")
        return None

    certs = db.relationship('Cert', secondary='job_cert', backref='job')


    
class JobCert(db.Model):
    # Connecting class to database table name
    __tablename__ = 'job_cert'    
    
    job = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    cert = db.Column(db.Integer, db.ForeignKey('cert.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    # relationship
    jobName = db.relationship('Job', backref='job_cert')
    certName = db.relationship('Cert', backref='job_cert')

class Role(db.Model):
    # Connecting class to database table name
    
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    avg_wage = db.Column(db.Numeric(5, 2), nullable=True)
    description = db.Column(db.Text, nullable=True)
