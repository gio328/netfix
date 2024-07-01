from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.utils.helpers import save_data_to_session
from flask_app.models.user import User


class Tvshow:
    DB = "nextfix" 
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.network = data.get('network')
        self.release_date = data.get('release_date')
        self.comments = data.get('comments')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.user_id = data.get('user_id')
        self.user = None

    @classmethod
    def save(cls, form_data):
        query = """
            INSERT INTO tvshows (title, network, release_date, comments, user_id) 
            VALUES (%(title)s, %(network)s, %(release_date)s, %(comments)s, %(user_id)s);
        """

        return connectToMySQL(cls.DB).query_db(query, form_data)

    @classmethod
    def get_show_by_title(cls, data):
        query = "SELECT * FROM tvshows WHERE title = %(title)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM tvshows;"
        results = connectToMySQL(cls.DB).query_db(query)
        shows = []
        for item in results:
            shows.append(cls(item))
        return shows

    @classmethod
    def get_show_with_id(cls, id):
        query = """
            SELECT * FROM tvshows
            JOIN users
            ON tvshows.user_id = users.id
            WHERE tvshows.id = %(id)s;
        """

        result = connectToMySQL(cls.DB).query_db(query, {'id': id})
        print('line 56 result => ', result)

        user = {
            'first_name': result[0].get('first_name'),
            'last_name': result[0].get('last_name')
        }

        tvshow_instance = cls(result[0])
        tvshow_instance.user = User(user)   

        return tvshow_instance


    @classmethod
    def delete_show(cls, id):
        query = "DELETE FROM tvshows WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, {'id': id})

    @classmethod
    def update_show(cls, data):
        query = """
            UPDATE tvshows
            SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, comments = %(comments)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate(form_data):
        is_valid = True
        print('validating form data => ', form_data)
        save_data_to_session(form_data)

        if form_data['title'] == "":
            flash("title is required")
            is_valid = False
        if form_data['network'] == "":
            flash("network is required")
            is_valid = False
        if form_data['release_date'] == "":
            flash("release date is required")
            is_valid = False
        if form_data['comments'] == "":
            flash("comments is required")
            is_valid = False
        if len(form_data['title']) < 3:
            flash("title must be at least 3 characters.")
            is_valid = False
        if len(form_data['network']) < 3:
            flash("Network must be at least 3 characters.")
            is_valid = False
        if len(form_data['comments']) < 3:
            flash("comments must be at least 3 characters.")
            is_valid = False

        return is_valid
    
    