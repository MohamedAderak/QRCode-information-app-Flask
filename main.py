from flask import Flask, render_template, request
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['database']

@app.route('/')
def home(id):
    return render_template('add_Person.html', id=id)
   
@app.route('/add_Person/<id>', methods=['POST'])
def add_Person(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        Person = {
            '$set': {
                'data': True,
                'Person': request.form['Person'],
                'Guardian': request.form['Guardian'],
                'Email': request.form['Email'],
                'Phone': request.form['Phone'],
                'gender': request.form['gender'],
                'Age': request.form['Age'],
                'Health': request.form['Health'],
                'address': request.form['address'],
                'Details': request.form['Details']
            }
        }
        db.Person.update_one({'_id': id}, Person)
        return display_Person(id)
    else:
       return "ERROR"




@app.route('/Person/<id>')
def display_Person(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is None or PersonId['data'] is False:
        return home(id)
    else:
        return render_template('display_Person.html', Person=PersonId)

        


if __name__ == '__main__':
    app.run(debug=True)
