from flask import Flask, render_template, request, session, redirect , url_for, make_response
from pymongo import MongoClient
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename
import re
import datetime



app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['database']
users = db["users"]


key = "26rhMqTw7I8YPvrtkovYrNWY-2hXEGhPuQSh76OGu_Q="
cipher = Fernet(key)


def encrypt_data(data):
    return cipher.encrypt(data.encode('utf-8'))


def decrypt_data(data):
    return cipher.decrypt(data).decode('utf-8')

def calculate_age(birth_date):
    birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
    current_date = datetime.date.today()
    age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age

@app.route('/')
def login():
        return render_template('/user/login.html', msg = '')

@app.route('/Home/<id>')
def home(id):
    PersonId = db.Person.find_one({'_id': id})    
    if PersonId is not None and PersonId['data'] is True:
        div_class = "error"
        return display(id, div_class)
    else :
        return render_template('index.html', id=id)

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page or any other page after logout
    return redirect('/login')

@app.route('/profil')
def user_interface(msg, username):
    return render_template('/user/user_interface.html', msg = msg, username = username)


def is_password_strong(password):
    return len(password) >= 8 and re.search(r'\d', password) and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password)

@app.route('/signup/<id>', methods=['POST'])
def signup(id):
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    existing_user = users.find_one({"email": email})
    existing_user_username = users.find_one({"username": username})
    if existing_user:
        return render_template('/user/inscription.html', id = id, msg='Email already exists')
    if existing_user_username:
            return render_template('/user/inscription.html', id = id, msg='Username already exists')
    if not is_password_strong(password):
            return render_template('/user/inscription.html', id = id, msg='Password is weak. Please choose a stronger password.')
    if password != confirm_password:
        return render_template('/user/inscription.html', id = id, msg='Passwords do not match')

    
    new_user = {
        'email': email,
        'user': username,
        'password': encrypt_data(password),
        'role': 'user',
        'personId': id
    }

    # Insert the new user document into the database
    users.insert_one(new_user)
    return redirect(url_for('home', id=id))


@app.route('/login', methods=['POST'])
def loginVerify():
    email = request.form['email']
    password = request.form['password']
    remember = request.form.get('remember')

    user = users.find_one({"email": email})
    if user and password == decrypt_data(user['password']):
        username = user['user']
        msg = "Login successful"
        if remember:
            resp = make_response(user_interface(msg, username))
            resp.set_cookie('email', email)
            return resp
        return user_interface(msg, username)
    else:
        return render_template('/user/login.html', msg = "Invalid email or password")
        


@app.route('/Person/<id>')
def inscription(id):
    PersonId = db.Person.find_one({'_id': id})    
    if PersonId is not None and PersonId['data'] is True:
        div_class = "error"
        return display(id, div_class)
    else :
         msg = ""
         return render_template('/user/inscription.html', id = id, msg = msg)
   
    


@app.route('/back/<id>', methods=['POST'])
def index(id):
    return render_template('index.html', id=id)

# old section
@app.route('/Old/<id>')
def Old(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        return formold(id)
    else:
        return "ERROR"
    
@app.route('/formold/<id>', methods=['POST'])
def formold(id):
    return render_template('/forms/formold.html', id=id)



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
                'city': encrypt_data(request.form['city']),
                'phone1': encrypt_data(request.form['phone1']),
                'phone2': encrypt_data(request.form['phone2']),
                'adress': encrypt_data(request.form['adress']),
                'image-old': encrypt_data(filepath),
                'email': encrypt_data(request.form['procheemail']),
                'potheseDentaire': encrypt_data(request.form['potheseDentaire']),
                'mutuelle': encrypt_data(request.form['mutuelle']),
                'Sourd': encrypt_data(request.form['Sourd']),
                'Malvoyant': encrypt_data(request.form['Malvoyant']),
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
        div_class = "error"
        return display(id, div_class)
    else:
        return "ERROR"


# child section
@app.route('/Child/<id>', methods=['get'])
def Child(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        return formchild(id)
    else:
        return "ERROR"

@app.route('/formchild/<id>', methods=['POST'])
def formchild(id):
    return render_template('/forms/formchild.html', id=id)


@app.route('/addchild/<id>', methods=['POST'])
def addchild(id):
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is not None:
        if request.files['image-child'] is not None:
            file = request.files['image-child']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['IMAGE_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
        else:
            filepath = "https://cdn-icons-png.flaticon.com/512/727/727399.png?w=740&t=st=1684162331~exp=1684162931~hmac=cfde87aafaa2bf3a10a42f594f2d3da822be8a843e6b8744b1ab7c0ad3b5a428"

        Person = {
            '$set': {
                'data': True,
                'model': "child",
                'nom': encrypt_data(request.form['nom']),
                'prenom': encrypt_data(request.form['prenom']),
                'email': encrypt_data(request.form['pere_email']),
                'image-child': encrypt_data(filepath),
                'birthday': encrypt_data(request.form['birthday']),
                'city': encrypt_data(request.form['city']),
                'adresse': encrypt_data(request.form['adresse']),
                'sanguin': encrypt_data(request.form['sanguin']),
                'Sourd': encrypt_data(request.form['Sourd']),
                'Malvoyant': encrypt_data(request.form['Malvoyant']),
                'phone1': encrypt_data(request.form['phone1']),
                'phone2': encrypt_data(request.form['phone2']),
                'poids': encrypt_data(request.form['poids']),
                'autremaladiecronique': encrypt_data(request.form['autremaladiecronique']),
                'maladieactuelle': encrypt_data(request.form['maladieactuelle']),
                'Traitementactuelle': encrypt_data(request.form['Traitementactuelle']),
                'autreallergies': encrypt_data(request.form['autreallergies']),
                'antecedchirurgicaux': encrypt_data(request.form['antecedchirurgicaux']),
                'chronique': encrypt_data(request.form['chronique']),
                'allergies': encrypt_data(request.form['allergies'])
            }
        }
        db.Person.update_one({'_id': id}, Person)
        div_class = "error"
        return display(id, div_class)
    else:
        return "ERROR"
    
# display section
@app.route('/display/<id>')
def display(id, div_class):
    if div_class:
        pass
    else:
        div_class = ""
    PersonId = db.Person.find_one({'_id': id})
    if PersonId is None or PersonId['data'] is False:
        return home(id)
    elif PersonId is not None and PersonId['data'] is True and PersonId['model'] == 'child':
         birth_date = decrypt_data(PersonId['birthday'])
         age = calculate_age(birth_date)
         Person = {
                'nom': decrypt_data(PersonId['nom']),
                'prenom': decrypt_data(PersonId['prenom']),
                'birthday': age,
                'city': decrypt_data(PersonId['city']),
                'phone1': decrypt_data(PersonId['phone1']),
                'phone2': decrypt_data(PersonId['phone2']),
                'adresse': decrypt_data(PersonId['adresse']),
                'image-child': decrypt_data(PersonId['image-child']),
                'email': decrypt_data(PersonId['email']),
                'Sourd': decrypt_data(PersonId['Sourd']),
                'Malvoyant': decrypt_data(PersonId['Malvoyant']),
                'poids': decrypt_data(PersonId['poids']),
                'autremaladiecronique': decrypt_data(PersonId['autremaladiecronique']),
                'maladieactuelle': decrypt_data(PersonId['maladieactuelle']),
                'Traitementactuelle': decrypt_data(PersonId['Traitementactuelle']),
                'autreallergies': decrypt_data(PersonId['autreallergies']),
                'antecedchirurgicaux': decrypt_data(PersonId['antecedchirurgicaux']),
                'sanguin': decrypt_data(PersonId['sanguin']),
                'chronique': decrypt_data(PersonId['chronique']),
                'allergies': decrypt_data(PersonId['allergies'])
         }
         return render_template('/display/display_child.html', id = id, Person=Person, div_class = div_class)
    
    elif PersonId is not None and PersonId['data'] is True and PersonId['model'] == 'old':
        birth_date = decrypt_data(PersonId['birthday'])
        age = calculate_age(birth_date)
        Person = {
                'nom': decrypt_data(PersonId['nom']),
                'prenom': decrypt_data(PersonId['prenom']),
                'birthday': age,
                'cin': decrypt_data(PersonId['cin']),
                'city': decrypt_data(PersonId['city']),
                'phone1': decrypt_data(PersonId['phone1']),
                'phone2': decrypt_data(PersonId['phone2']),
                'adress': decrypt_data(PersonId['adress']),
                'image-old': decrypt_data(PersonId['image-old']),
                'email': decrypt_data(PersonId['email']),
                'potheseDentaire': decrypt_data(PersonId['potheseDentaire']),
                'mutuelle': decrypt_data(PersonId['mutuelle']),
                'Sourd': decrypt_data(PersonId['Sourd']),
                'Malvoyant': decrypt_data(PersonId['Malvoyant']),
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
        return render_template('/display/display_old.html', id = id, Person=Person, div_class = div_class)
    else:
        return "ERROR"
        

@app.route('/verify_code/<id>', methods=['POST'])
def verify_code(id):
    entered_code = request.form['codeInput']

    # Query the database to check if the code exists
    # code = db.Person.find_one({'code': entered_code})

    if entered_code == "12345":
        # Code exists, change the class of the div to 'success'
        div_class = 'success'
    else:
        # Code does not exist, change the class of the div to 'error'
        div_class = 'error'

    return display(id, div_class)



if __name__ == '__main__':
    app.config['IMAGE_FOLDER'] = '/static/images'
    app.run(debug=True)
