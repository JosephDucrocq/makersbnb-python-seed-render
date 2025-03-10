from lib.space import Space

def test_space_can_instantiate():
    space = Space(None, "Name", "Location", "Description", True, 50, 1)
    assert space.id == None
    assert space.name == "Name"
    assert space.location == "Location"
    assert space.description == "Description"
    assert space.availability == True
    assert space.price_per_night == 50
    assert space.user_id == 1

def test_2_identical_spaces_are_equal():
    space1 = Space(None, "Name", "Location", "Description", True, 50, 1)
    space2 = Space(None, "Name", "Location", "Description", True, 50, 1)
    assert space1 == space2

def test_space_repr_looks_nice():
    space = Space(None, "Buckingham Palace", "London", "It's a palace", True, 5, 1)
    assert repr(space) == '''Space(ID: None, Name: Buckingham Palace, Location: London, Description: It's a palace, Availability: True, Price: 5, User_ID: 1)'''
