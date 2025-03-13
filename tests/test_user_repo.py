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
        User(1, "Luis", "f5d44b29add0d1a87b9edc82e7c5a9fd"),
        User(2, "Joseph", "6380dcbb2728aa384ed16fc1cf98b1f0"),
        User(3, 'jackmisner', '5e075470c9298a362f78901a75c0d288')
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
        User(1, "Luis", "f5d44b29add0d1a87b9edc82e7c5a9fd"),
        User(2, "Joseph", "6380dcbb2728aa384ed16fc1cf98b1f0"),
        User(3, 'jackmisner', '5e075470c9298a362f78901a75c0d288'),
        User(4, 'test user', 'b3d34352fc26117979deabdf1b9b6354')
    ]


"""
When I call #find for a username
I get the user name
"""


def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = UserRepository(db_connection)
    #add username, password
    result = repository.find_by_username("Luis")
    assert str(result) == '''User(ID: 1, Username: Luis, Encrypted Password: f5d44b29add0d1a87b9edc82e7c5a9fd)''' 
