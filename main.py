from flask import Flask, render_template, request
from pymongo import MongoClient
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['database']



key = "26rhMqTw7I8YPvrtkovYrNWY-2hXEGhPuQSh76OGu_Q="
cipher = Fernet(key)


def encrypt_data(data):
    return cipher.encrypt(data.encode('utf-8'))


def decrypt_data(data):
    return cipher.decrypt(data).decode('utf-8')


@app.route('/Person/<id>')
def home(id):
    PersonId = db.Person.find_one({'_id': id})    
    if PersonId is not None and PersonId['data'] is True:
        return display(id)
    else :
        return render_template('index.html', id=id)


@app.route('/back/<id>', methods=['POST'])
def index(id):
    return render_template('index.html', id=id)

# old section
@app.route('/Old/<id>', methods=['POST'])
def Old(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        return formold(id)
    else:
        return "ERROR"
    
@app.route('/formold/<id>', methods=['POST'])
def formold(id):
    return render_template('formold.html', id=id)



@app.route('/addold/<id>', methods=['POST'])
def addold(id):
    PersonId = db.Person.find_one({'_id': id})
    
    if PersonId is not None:
        if request.files['image-old'] is None:
            file = request.files['image-old']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['IMAGE_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
        else:
            filepath = "https://cdn-icons-png.flaticon.com/512/727/727399.png?w=740&t=st=1684162331~exp=1684162931~hmac=cfde87aafaa2bf3a10a42f594f2d3da822be8a843e6b8744b1ab7c0ad3b5a428"
        
        Person = {
            '$set': {
                'data': True,
                'model': "old",
                'nom': encrypt_data(request.form['nom']),
                'prenom': encrypt_data(request.form['prenom']),
                'birthday': encrypt_data(request.form['birthday']),
                'cin': encrypt_data(request.form['cin']),
                'phone1': encrypt_data(request.form['phone1']),
                'phone2': encrypt_data(request.form['phone2']),
                'adress': encrypt_data(request.form['adress']),
                'image-old': encrypt_data(filepath),
                'email': encrypt_data(request.form['email']),
                'potheseDentaire': encrypt_data(request.form['potheseDentaire']),
                'mutuelle': encrypt_data(request.form['mutuelle']),
                'sourd&malvoyant': encrypt_data(request.form['sm']),
                'poids': encrypt_data(request.form['poids']),
                'autremaladiecronique': encrypt_data(request.form['autremaladiecronique']),
                'maladieactuelle': encrypt_data(request.form['maladieactuelle']),
                'Traitementactuelle': encrypt_data(request.form['Traitementactuelle']),
                'autreallergies': encrypt_data(request.form['autreallergies']),
                'antecedmedicaux': encrypt_data(request.form['antecedmedicaux']),
                'antecedchirurgicaux': encrypt_data(request.form['antecedchirurgicaux']),
                'sanguin': encrypt_data(request.form['sanguin']),
                'chronique': encrypt_data(request.form['chronique']),
                'allergies': encrypt_data(request.form['allergies']),
                'pothesetitanique': encrypt_data(request.form['pothesetitanique'])
            }
        }
        db.Person.update_one({'_id': id}, Person)
        return display(id)
    else:
        return "ERROR"


# child section
@app.route('/Child/<id>', methods=['POST'])
def Child(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        return formchild(id)
    else:
        return "ERROR"

@app.route('/formchild/<id>', methods=['POST'])
def formchild(id):
    return render_template('formchild.html', id=id)


@app.route('/addchild/<id>', methods=['POST'])
def addchild(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        if request.files['image'] is None:
            file = request.files['image']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['IMAGE_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
        else:
            filepath = "https://cdn-icons-png.flaticon.com/512/727/727399.png?w=740&t=st=1684162331~exp=1684162931~hmac=cfde87aafaa2bf3a10a42f594f2d3da822be8a843e6b8744b1ab7c0ad3b5a428"

        Person = {
            '$set': {
                'data': True,
                'model': "child",
                'First_name': encrypt_data(request.form['nom']),
                'Last_name': encrypt_data(request.form['prenom']),
                'Email': encrypt_data(request.form['email']),
                'Image': encrypt_data(filepath),
                'Mother_name': encrypt_data(request.form['mother']),
                'Father_name': encrypt_data(request.form['father']),
                'date_Naissance': encrypt_data(request.form['dateNaissance']),
                'Adress': encrypt_data(request.form['adress']),
                'sanguin': encrypt_data(request.form['sanguin']),
                'more': encrypt_data(request.form['more']),
                'Mother_Phone': encrypt_data(request.form['phone']),
                'Father_Phone': encrypt_data(request.form['phone2'])
            }
        }
        db.Person.update_one({'_id': id}, Person)
        return display(id)
    else:
        return "ERROR"
    
# display section
@app.route('/display/<id>')
def display(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is None or PersonId['data'] is False:
        return home(id)
    elif PersonId is not None and PersonId['data'] is True and PersonId['model'] == 'child':
         Person = {
                'First_name': decrypt_data(PersonId['First_name']),
                'Last_name': decrypt_data(PersonId['Last_name']),
                'Email': decrypt_data(PersonId['Email']),
                'Image': decrypt_data(PersonId['Image']),
                'Mother_name': decrypt_data(PersonId['Mother_name']),
                'Father_name': decrypt_data(PersonId['Father_name']),
                'date_Naissance': decrypt_data(PersonId['date_Naissance']),
                'Adress': decrypt_data(PersonId['Adress']),
                'sanguin': decrypt_data(PersonId['sanguin']),
                'more': decrypt_data(PersonId['more']),
                'Mother_Phone': decrypt_data(PersonId['Mother_Phone']),
                'Father_Phone': decrypt_data(PersonId['Father_Phone'])
         }
         return render_template('display_child.html', Person=Person)
    
    elif PersonId is not None and PersonId['data'] is True and PersonId['model'] == 'old':
        Person = {
                'nom': decrypt_data(PersonId['nom']),
                'prenom': decrypt_data(PersonId['prenom']),
                'birthday': decrypt_data(PersonId['birthday']),
                'cin': decrypt_data(PersonId['cin']),
                'phone1': decrypt_data(PersonId['phone1']),
                'phone2': decrypt_data(PersonId['phone2']),
                'adress': decrypt_data(PersonId['adress']),
                'image-old': decrypt_data(PersonId['image-old']),
                'email': decrypt_data(PersonId['email']),
                'potheseDentaire': decrypt_data(PersonId['potheseDentaire']),
                'mutuelle': decrypt_data(PersonId['mutuelle']),
                'sourd&malvoyant': decrypt_data(PersonId['sourd&malvoyant']),
                'poids': decrypt_data(PersonId['poids']),
                'autremaladiecronique': decrypt_data(PersonId['autremaladiecronique']),
                'maladieactuelle': decrypt_data(PersonId['maladieactuelle']),
                'Traitementactuelle': decrypt_data(PersonId['Traitementactuelle']),
                'autreallergies': decrypt_data(PersonId['autreallergies']),
                'antecedmedicaux': decrypt_data(PersonId['antecedmedicaux']),
                'antecedchirurgicaux': decrypt_data(PersonId['antecedchirurgicaux']),
                'sanguin': decrypt_data(PersonId['sanguin']),
                'chronique': decrypt_data(PersonId['chronique']),
                'allergies': decrypt_data(PersonId['allergies']),
                'pothesetitanique': decrypt_data(PersonId['pothesetitanique'])
            }
        return render_template('display_old.html', Person=Person)
    else:
        return "ERROR"
        


if __name__ == '__main__':
    app.config['IMAGE_FOLDER'] = '/static/images'
    app.run(debug=True)
