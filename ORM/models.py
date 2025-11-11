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
    compnay = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    
class Contract(db.Model):
    # Connecting class to database table name
    __tablename__ = 'contract'

    id = db.Column(db.Integer, db.ForeignKey("job.id"), primary_key=True, autoincrement=True)
    terms =  db.Column(db.Text, nullable=True)
    schedule =  db.Column(db.Text, nullable=True)
    pay =  db.Column(db.Text, nullable=True)
    
class Ft(db.Model):
    # Connecting class to database table name
    __tablename__ = 'full_time'
    
    id = db.Column(db.Integer, db.ForeignKey("job.id"), primary_key=True, autoincrement=True)
    hourly =  db.Column(db.Numeric(4,2), nullable=True)
    schedule =  db.Column(db.Text, nullable=True)
    benefits =  db.Column(db.Text, nullable=True)
    
class Pt(db.Model):
    # Connecting class to database table name
    __tablename__ = 'part_time'

    id = db.Column(db.Integer, db.ForeignKey("job.id"), primary_key=True, autoincrement=True)
    hourly =  db.Column(db.Numeric(4, 2), nullable=True)
    schedule =  db.Column(db.Text, nullable=True)

class Job(db.Model):
    # Connecting class to database table name
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.Date, nullable=True)
    close_date = db.Column(db.Date, nullable=True)
    hyperlink = db.Column(db.Text, nullable=True)
    company = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    contact = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=True)
    
class JobCert(db.Model):
    # Connecting class to database table name
    __tablename__ = 'job_cert'    
    
    job = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True, nullable=False)
    cert = db.Column(db.Integer, db.ForeignKey('cert.id'), primary_key=True, nullable=False)

class Role(db.Model):
    # Connecting class to database table name
    
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    avg_wage = db.Column(db.Numeric(5, 2), nullable=True)
    description = db.Column(db.Text, nullable=True)
