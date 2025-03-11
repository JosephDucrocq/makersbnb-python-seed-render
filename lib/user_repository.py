from lib.user import User


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        return ", ".join([row["username"] for row in rows])

    def create(self, user):
        self._connection.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            [user.username, user.password],
        )
        return None

    def find(self, id):
        rows = self._connection.execute("SELECT * from users WHERE id = %s", [id])
        row = rows[0]
        return User(row["id"], row["username"], row["password"])
    
    def find_by_username(self, username: str):
        rows = self._connection.execute("SELECT * from users WHERE username = %s", [username])
        row = rows[0]
        return User(row["id"], row["username"], row["password"])
