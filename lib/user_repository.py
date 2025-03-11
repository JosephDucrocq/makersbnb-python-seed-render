from lib.user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        return [User(row["id"], row["username"], row["password"]) for row in rows]

    def create(self, user):
        if self._isUserUnique(user.username):  
            self._connection.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                [user.username, user.password],
            )
        return None
    
    def _isUserUnique(self, username):
        if username in self.list_all_usernames():
            return False
        else:
            return True

    def find_by_id(self, id: int):
        rows = self._connection.execute("SELECT * from users WHERE id = %s", [id])
        row = rows[0]
        return User(row["id"], row["username"], row["password"])
    
    def find_by_username(self, username: str):
        rows = self._connection.execute("SELECT * from users WHERE username = %s", [username])
        row = rows[0]
        return User(row["id"], row["username"], row["password"])
    
    def list_all_usernames(self):
        usernames = []
        for user in self.all():
            usernames.append(user.username)
        return usernames
