from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    db = 'coding_dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.creator = data['first_name']
        self.created_at = data['created_at']

    @staticmethod
    def create(form_data, user_id):
        query = """
            INSERT INTO COMMENTS
            (comment, user_id, post_id)
            VALUES
            (%(comment)s, %(user_id)s, %(post_id)s);
        """

        data = {
            'comment': form_data['comment'],
            'user_id': user_id,
            'post_id': form_data['post_id']
        }

        comment_id = connectToMySQL('coding_dojo_wall_schema').query_db(query, data)

        return comment_id
    

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM COMMENTS
            LEFT JOIN users
            ON comments.user_id = users.id
            JOIN posts
            ON comments.post_id = posts.id;
        """

        results = connectToMySQL('coding_dojo_wall_schema').query_db(query)

        all_comments = []

        for comment in results:
            all_comments.append(cls(comment))

        return all_comments


    @staticmethod
    def delete(form_data):
        query = """
            DELETE FROM comments
            WHERE id = %(comment_id)s;
        """
        connectToMySQL('coding_dojo_wall_schema').query_db(query, form_data)