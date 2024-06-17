from route_function import get_db_connection
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, fullname, email, password):
        self.id = str(user_id)
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password


    def user_get_id(user_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE user_id = %s", (
                user_id,
            )
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()
        return user


    @staticmethod
    def get(user_id):
        try:
            user = User.user_get_id(user_id)
            if user:
                return User(
                    user['user_id'],
                    user['username'],
                    user['fullname'],
                    user['email'],
                    user['password']
                )
            return None
        except Exception as e:
            print("{}: {}".format(Exception, e))
            return None
