from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.post import Post
from pprint import pprint

@app.route('/create_post', methods=['POST'])
def create_post():
    if not Post.validate_post(request.form):
        session['create_post_data'] = request.form
        return redirect(url_for('display_user_wall'))
    # If form data passes validation, create post
    if 'create_post_data' in session:
        session.pop('create_post_data')
    user_id = session['logged_in_user_id']
    print(f'The logged in user id is {user_id}')
    Post.create(request.form, user_id)
    return redirect(url_for('display_user_wall'))

@app.route('/delete_post', methods=['POST'])
def delete_post():
    pprint(request.form)
    Post.delete(request.form)
    return redirect(url_for('display_user_wall'))