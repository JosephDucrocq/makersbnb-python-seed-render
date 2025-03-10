from lib.space_repository import SpaceRepository
from lib.space import Space

def test_all_returns_all_spaces(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = SpaceRepository(db_connection)
    spaces = repository.all()
    assert spaces == [Space(1, 'Makers Villa', 'London', 'Beautiful refurbished industrial warehouse', True, 150, 1), Space(2, 'Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', True, 90, 2)]

def test_find_returns_specific_space(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = SpaceRepository(db_connection)
    space = repository.find(1)
    assert space == Space(1, 'Makers Villa', 'London', 'Beautiful refurbished industrial warehouse', True, 150, 1)
    space = repository.find(2)
    assert space == Space(2, 'Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', True, 90, 2)

def test_can_create_new_space(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = SpaceRepository(db_connection)
    new_space = Space(None, 'new space', 'england', 'its a bit wet', True, 0, 2)
    repository.create(new_space)
    spaces = repository.all()
    assert spaces == [Space(1, 'Makers Villa', 'London', 'Beautiful refurbished industrial warehouse', True, 150, 1), Space(2, 'Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', True, 90, 2), Space(3, 'new space', 'england', 'its a bit wet', True, 0, 2)]

def test_can_delete_space(db_connection):
    db_connection.seed("seeds/makers_bnb_Bowie.sql")
    repository = SpaceRepository(db_connection)
    repository.delete(1)
    spaces = repository.all()
    assert spaces == [Space(2, 'Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', True, 90, 2)]
