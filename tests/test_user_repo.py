from lib.user_repository import UserRepository
from lib.user import User

"""
When I call #all
I get all the users in the users table
"""


def test_all(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    assert repository.all() == "Luis, Joseph"


"""
When I call #create for an user
Nothing is returned
When I call #all again
I get all the users in the users table
"""


def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    user = User(1, "test user", "1234pass")
    repository.create(user)
    assert repository.all() == "Luis, Joseph, test user"


"""
When I call #find for an user id
I get the user name
"""


def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    result = repository.find(1)
    assert result == User(1, "Luis", "IloveTaylorSwift")
