from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Post:
    db = 'coding_dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM posts
            LEFT JOIN users
            ON posts.user_id = users.id
            ORDER BY posts.created_at DESC
        """

        results = connectToMySQL(cls.db).query_db(query)

        all_posts = []

        for row in results:
            post = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password']
            }
            user_obj = User(user_data)
            post.creator = user_obj
            all_posts.append(post)

        return all_posts

    @staticmethod
    def create(form_data, user_id):
        query = """
            INSERT INTO posts
            (content, user_id)
            VALUES (%(content)s, %(user_id)s);
        """

        data = {
            'content': form_data['content'],
            'user_id': user_id
        }

        post_id = connectToMySQL('coding_dojo_wall_schema').query_db(query, data)

        return post_id
    

    @staticmethod
    def delete(form_data):
        query = """
            DELETE FROM posts
            WHERE id = %(post_id)s;
        """
        connectToMySQL('coding_dojo_wall_schema').query_db(query, form_data)

    @classmethod
    def validate_post(cls, form_data):
        is_valid = True

        if not form_data['content']:
            flash('Post content cannot be blank', 'create_post')
            is_valid = False

        return is_valid