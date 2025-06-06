from lib.user import User
import hashlib
class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        return [User(row["id"], row["username"], row["encrypted_password"]) for row in rows]

    def create(self, user):
        if self._isUserUnique(user.username):  
            self._connection.execute(
                "INSERT INTO users (username, encrypted_password) VALUES (%s, %s)",
                [user.username, user.encrypted_password],
            )
        return None
    
    def _isUserUnique(self, username):
        if username in self.list_all_usernames():
            return False
        else:
            return True

    def find_by_id(self, id: int):
        rows = self._connection.execute("SELECT * from users WHERE id = %s", [id])
        if len(rows) == 0:
            return None
        row = rows[0]
        return User.from_database(row["id"], row["username"], row["encrypted_password"])
    
    def find_by_username(self, username: str):
        rows = self._connection.execute("SELECT * from users WHERE username = %s", [username])
        if len(rows) == 0:
            return None
        row = rows[0]
        return User.from_database(row["id"], row["username"], row["encrypted_password"])
    
    def list_all_usernames(self):
        usernames = []
        for user in self.all():
            usernames.append(user.username)
        return usernames
    
    def check_password(self, username: str, unencrypted_password: str) -> bool:
            password_hash = hashlib.md5(unencrypted_password.encode()).hexdigest()
            test_user = self.find_by_username(username)
            if not isinstance(test_user, User):
                return False
            return test_user.encrypted_password == password_hash