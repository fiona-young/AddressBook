#!flask/bin/python
from flask import Flask, jsonify, abort
from crossdomain import crossdomain
from database import Database


root = "/address/api/v1.0/"
app = Flask(__name__)

people = [
    {'id': 1,
     'main': {
         'first_name': "John",
         'second_name': "Doe",
         'email': "john.doe@company.com",
         'phone': "0134543"
     },
     'address': {
         'line1': "line1",
         'line2': "line2",
         'country': "UK",
         'postcode': "EH73RT"
     }}, {'id': 2,
          'main': {
              'first_name': "Jane",
              'second_name': "Pratt",
              'email': "jane.pratt@company.com",
              'phone': "14567"
          },
          'address': {
              'line1': "Front",
              'line2': "Back",
              'country': "UK",
              'postcode': "Edinburgh"
          }},
]

@app.route(root+'people/', methods=['GET'])
@crossdomain(origin='*')
def get_people():
    try:
        db = Database()
        people = db.get_people()
        return jsonify({'people': people})
    except:
        abort(500)


@app.route(root+'people/<int:person_id>', methods=['GET'])
@crossdomain(origin='*')
def get_person(person_id):
    try:
        db = Database()
        person = db.get_person(person_id)
        return jsonify({'person': person})
    except:
        abort(500)

@app.route(root+'companies/', methods=['GET'])
@crossdomain(origin='*')
def get_companies():
    try:
        db = Database()
        companies = db.get_companies()
        return jsonify({'companies': companies})
    except:
        abort(500)

@app.route(root+'companies/<int:company_id>', methods=['GET'])
@crossdomain(origin='*')
def get_company(company_id):
    try:
        db = Database()
        company = db.get_company(company_id)
        return jsonify({'company': company})
    except:
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)