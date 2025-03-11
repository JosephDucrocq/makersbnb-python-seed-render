from lib.user_repository import UserRepository
from lib.user import User
import pytest

"""
When I call #all
I get all the users in the users table
"""


def test_all(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    assert repository.all() == [
        User(1, "Luis", "IloveTaylorSwift"),
        User(2, "Joseph", "Idoto")
    ]


"""
When I call #create for an user
Nothing is returned
When I call #all again
I get all the users in the users table
"""


def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    user = User(None, "test user", "1234pass")
    repository.create(user)
    assert repository.all() == [
        User(1, "Luis", "IloveTaylorSwift"),
        User(2, "Joseph", "Idoto"), 
        User(3, "test user", "1234pass")
    ]

"""
When I call #create for an existing user
An error message appears
"""


def test_create_existing_user_throws_exception(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    user = User(1, "Luis", "IloveTaylorSwift")
    with pytest.raises(ValueError) as e:
        repository.create(user)
    assert str(e.value) == "Username Already exists!"
    assert repository.all() == [
        User(1, "Luis", "IloveTaylorSwift"),
        User(2, "Joseph", "Idoto"), 
    ]


"""
When I call #find for a username
I get the user name
"""


def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    #add username, password
    result = repository.find("Luis")
    assert result == User(1, "Luis", "IloveTaylorSwift")
