#!flask/bin/python
from flask import Flask, jsonify, abort, request
from crossdomain import crossdomain
from database import Database


root = "/address/api/v1.0/"
app = Flask(__name__)

@app.route(root+'people/', methods=['GET'])
@crossdomain(origin='*')
def get_people():
    db = Database()
    people = db.get_people()
    return jsonify({'people': people})

@app.route(root+'people/<int:person_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_person(person_id):
    db = Database()
    db.delete_person(person_id)
    return jsonify({'success': True})


@app.route(root+'people/<int:person_id>', methods=['OPTIONS'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def preflight_people_id():
    pass

@app.route(root+'people/<int:person_id>', methods=['GET'])
@crossdomain(origin='*')
def get_person(person_id):
    try:
        db = Database()
        person = db.get_person(person_id)
        return jsonify({'person': person})
    except:
        abort(500)

@app.route(root+'people/', methods=['PUT'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def put_people():
    if not request.json:
        abort(400)
    people = request.json
    if len(people)>0:
        db = Database()
        for person in people:
            if 'item_id' not in person:
                db.add_person(person)
            else:
                db.update_person(person)
    return jsonify({'success': True})

@app.route(root+'people/', methods=['OPTIONS'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def preflight_people():
    pass

@app.route(root+'companies/', methods=['GET'])
@crossdomain(origin='*')
def get_companies():
    db = Database()
    companies = db.get_companies()
    return jsonify({'companies': companies})

@app.route(root+'companies/', methods=['PUT'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def put_companies():
    if not request.json:
        abort(400)
    companies = request.json
    if len(companies)>0:
        db = Database()
        for company in companies:
            if 'item_id' not in company:
                db.add_company(company)
            else:
                db.update_company(company)
    return jsonify({'success': True})

@app.route(root+'companies/', methods=['OPTIONS'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def preflight_companies():
    pass

@app.route(root+'companies/<int:company_id>', methods=['GET'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def get_company(company_id):
    db = Database()
    company = db.get_company(company_id)
    return jsonify({'company': company})


@app.route(root+'companies/<int:company_id>', methods=['DELETE'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def delete_company(company_id):
    db = Database()
    db.delete_company(company_id)
    return jsonify({'success': True})

@app.route(root+'companies/<int:company_id>', methods=['OPTIONS'])
@crossdomain(origin='*',headers="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
def preflight_company_id():
    pass



if __name__ == '__main__':
    app.run(debug=True)