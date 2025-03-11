from lib.user import User


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        return [User(row["id"], row["username"], row["password"]) for row in rows]

    def create(self, user):
        if not self._isUserUnique(user.username):  
            self._connection.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                [user.username, user.password],
            )
        return None
    
    def _isUserUnique(self, username):
        for user in self.all():
            if username in user.username:
                raise ValueError("Username Already exists!")


    def find(self, username):
        rows = self._connection.execute("SELECT * from users WHERE username = %s", [username])
        row = rows[0]
        return User(row["id"], row["username"], row["password"])
