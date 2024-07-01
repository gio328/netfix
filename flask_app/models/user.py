
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.utils.helpers import save_data_to_session
from datetime import date
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#Password must have at least 1 number and 1 uppercase letter
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])')



class User:
    DB = "nextfix" 
    def __init__(self, data):
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')


    # Create Users Models
    @classmethod
    def save(cls, form_data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        }

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]

    @staticmethod
    def validate(data):
        is_valid = True
        print('validating form data => ', data)
        save_data_to_session(data)

        if data['first_name'] == "":
            flash("First Name is required")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if data['last_name'] == "":
            flash("Last Name is required")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if data['email'] == "":
            flash("Email is required")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        if data['password'] == "":
            flash("password is required")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if data['confirm_password'] != data['password']:
            flash("Passwords do not match")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("Password must have at least 1 number and 1 uppercase letter")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if data['email'] == "":
            flash("Invalid Email/Password")
            is_valid = False
        if data['password'] == "":
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid

