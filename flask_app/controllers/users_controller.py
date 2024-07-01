from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from functools import wraps
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        if not User.validate(form_data): #validate form data
            return redirect('/')

        if email_exist(form_data): #check if email already exists
            return redirect('/')

        store_user_in_session(form_data)
        delete_session_data()
        result = User.save(form_data) #save to database returns id
        # print('result => ', result)
        save_id_to_session(result)
        return redirect('/shows')
    else:
        return render_template('/index.html')

@app.route('/login', methods=['POST'])      
def login():
    delete_session_data()
    form_data = request.form.to_dict()
    if not User.validate_login(form_data):
        return redirect('/')

    user_in_db = User.get_user_by_email(form_data)

    if not user_in_db: #check if user exists
        flash('Invalid Email/Password')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db['password'], form_data['password']): #check if password matches
        flash('Invalid Email/Password')
        return redirect('/')

    store_user_in_session(user_in_db) #store user in session
    return redirect('/shows')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def email_exist(form_data):
    result = User.get_user_by_email(form_data)#return false or data
    if not result:
        return False
    if 'email' in result:
        flash('Email already exists')
        return True

def save_id_to_session(result):
    if result:
        session['loggedin.id'] = result


def delete_session_data():
    if 'first_name' in session:
        del session['first_name']
    if 'last_name' in session:
        del session['last_name']
    if 'email' in session:
        del session['email']
        
def store_user_in_session(data):
    if 'id' in data:
        session['loggedin.id'] = data['id']
    if 'first_name' in data:
        session['loggedin.first_name'] = data['first_name']
    if 'last_name' in data:
        session['loggedin.last_name'] = data['last_name']
