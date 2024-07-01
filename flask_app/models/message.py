from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Message:
    DB = 'nextfix'
    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.tvshow_id = data.get('tvshow_id')
        self.message = data.get('message')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.user= None

    @classmethod
    def get_messages(cls, id):
        query = """
            SELECT * FROM messages
            JOIN users
            ON messages.user_id = users.id
            WHERE tvshow_id = %(id)s
            ORDER BY messages.id desc;
        """

        result = connectToMySQL(cls.DB).query_db(query, {'id': id})
        print('line 26 result => ', result)

        messages = []
        for row in result:
            user = {
                'id': row.get('user_id'),
                'first_name': row.get('first_name'),
                'last_name': row.get('last_name'),
            }

            message = {
                'id': row.get('id'),
                'user_id': row.get('user_id'),
                'tvshow_id': row.get('tvshow_id'),
                'message': row.get('message'),
                'created_at': row.get('created_at'),
                'updated_at': row.get('updated_at')
            }
            
            message_instance = cls(message)
            message_instance.user = User(user)
            messages.append(message_instance)

        return messages

    @classmethod
    def post_message(cls, data):
        query = """
            INSERT INTO messages (user_id, tvshow_id, message)
            VALUES (%(user_id)s, %(tvshow_id)s, %(message)s);
        """

        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def delete_comment(cls, id):
        query = """
            DELETE FROM messages
            WHERE id = %(id)s
        """

        return connectToMySQL(cls.DB).query_db(query, {'id': id})

    # ========================== Flashcard ==========================
    
