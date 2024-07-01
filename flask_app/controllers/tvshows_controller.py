from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.utils.helpers import login_required
from flask_app.models.tvshow import Tvshow
from flask_app.models.message import Message
from functools import wraps

@app.route('/shows')
@login_required
def shows():
    result = Tvshow.get_all_shows()
    return render_template('shows.html',  shows=result)

@app.route('/shows/new')
@login_required
def new_show():
    return render_template('new.html')

@app.route('/shows/new', methods=['POST'])
@login_required
def add_new_show():
    form_data = request.form.to_dict()
    if not Tvshow.validate(form_data):
        return redirect('/shows/new')
    if title_exist(form_data): #check if title already exists
        return redirect('/shows/new')
    Tvshow.save(form_data)
    delete_session()
    return redirect('/shows')

@app.route('/shows/<int:id>')
@login_required
def details(id):
    show_details = Tvshow.get_show_with_id(id)
    messages = Message.get_messages(id)
    return render_template('details.html', show=show_details, messages=messages)

@app.route('/shows/<int:id>', methods=['POST'])
@login_required
def post_message(id):
    form_data = request.form.to_dict()
    Message.post_message(form_data)
    return redirect('/shows/'+str(id))

@app.route('/delete_comment/<int:msg_id>/<int:user_id>/<int:id>/')
@login_required
def delete_comment(msg_id, user_id, id):
    if session['loggedin.id'] != user_id:
        return redirect('/shows')
    Message.delete_comment(msg_id)
    return redirect('/shows/'+str(id))

@app.route('/shows/edit/<int:id>')
@login_required
def edit_show(id):
    show_details = Tvshow.get_show_with_id(id)
    return render_template('edit.html', show=show_details)

@app.route('/update_show', methods=['POST'])
@login_required
def update_show():
    form_data = request.form.to_dict()
    if not Tvshow.validate(form_data):
        return redirect('/shows/edit/'+form_data['id'])
    
    Tvshow.update_show(form_data)
    delete_session()
    return redirect('/shows')

@app.route('/shows/delete/<int:id>')
@login_required
def delete_show(id):
    Tvshow.delete_show(id)
    return redirect('/shows')

# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     print("file: ", file)
#     if file:
#         file.save('flask_app/static/uploads/'+file.filename)
#     return redirect('/shows')


def title_exist(form_data):
    result = Tvshow.get_show_by_title(form_data)
    if not result:
        return False
    if 'title' in result:
        flash('Title already exists')
        return True

def delete_session():
    if 'title' in session:
        session.pop('title')
    if 'network' in session:
        session.pop('network')
    if 'release_date' in session:
        session.pop('release_date')
    if 'comments' in session:
        session.pop('comments')
    

