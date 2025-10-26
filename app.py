#! /usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

companies = [
    {'name': 'Gr8ttek',
     'industry': 'Service',
     'location': 'Cheyenne, WY',
     'size': '11-50',
     'website': 'https://rksbh.com'
    },
    {'name': 'Communication Resources',
     'industry': 'Service',
     'location': '5340 Moment Rd, Missoula, MT 59808',
     'size': '11-50',
     'website': 'https://communicationres.com'
    }]

@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/about')
def about():
    return(render_template('about.html'))

@app.route('/premade')
def premade():
    output = render_template('static.html')
    return output

@app.route('/companies')
def viewCompanies():
    output = render_template('viewCompanies.html', companies=companies)
    return output

@app.route('/addCompany')
def addCompany():
    output = render_template('addCompany.html')
    return output

@app.route('/addCompanyToList', methods=['GET'])
def addCompanyToList():

    new_company = {
        'name': request.args.get('name'),
        'industry': request.args.get('industry'),
        'location': request.args.get('location'),
        'size': request.args.get('size'),
        'website': request.args.get('website')
        }

    companies.append(new_company)

    return redirect(url_for('viewCompanies'))

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
