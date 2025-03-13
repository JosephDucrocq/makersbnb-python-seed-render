import hashlib
class User:
    def __init__(self, id: int, username: str, unencrypted_password: str):
        self.id = id
        self.username = username
        self.encrypted_password = hashlib.md5(unencrypted_password.encode()).hexdigest()

    def __repr__(self):
        return (
            f"User(ID: {self.id}, Username: {self.username}, Encrypted Password: {self.encrypted_password})"
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def from_database(cls, id: int, username: str, encrypted_password: str):
        """
        Alternative constructor for creating a User from database data
        Allows direct creation with a pre-existing hash
        """    
        # Create a new instance
        instance = cls.__new__(cls)
        
        # Set attributes directly
        instance.id = id
        instance.username = username
        instance.encrypted_password = encrypted_password        
        return instance