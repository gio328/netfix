from flask_app import app
from flask import session, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin.first_name' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def save_data_to_session(data):
    session['title'] = data.get('title') or ""
    session['network'] = data.get('network') or ""
    session['release_date'] = data.get('release_date') or ""
    session['comments'] = data.get('comments') or ""

