from flask_app import app   
from flask import redirect, request, session, url_for
from flask_app.models.comment import Comment

@app.route('/create_comment', methods=['POST'])
def create_comment():
    user_id = session['logged_in_user_id']
    Comment.create(request.form, user_id)
    return redirect(url_for('display_user_wall'))

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    Comment.delete(request.form)
    return redirect(url_for('display_user_wall'))