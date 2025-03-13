from lib.space import Space

def test_space_can_instantiate():
    space = Space(None, "Name", "Location", "Description",45, "2025-03-01", "2025-03-03", "https://www.google.com", 1)
    assert space.id == None
    assert space.name == "Name"
    assert space.location == "Location"
    assert space.description == "Description"
    assert space.dates_available_dict == {"2025-03-01": True, "2025-03-02": True, "2025-03-03": True}
    assert space.price_per_night == 45
    assert space.image_content == "https://www.google.com"
    assert space.user_id == 1

def test_2_identical_spaces_are_equal():
    space1 = Space(None, "Name", "Location", "Description",45, "2025-03-01", "2025-03-03", "https://www.google.com", 1)
    space2 = Space(None, "Name", "Location", "Description",45, "2025-03-01", "2025-03-03", "https://www.google.com", 1)
    assert space1 == space2

def test_space_repr_looks_nice():
    space = Space(None, "Buckingham Palace", "London", "It's a palace",45, "2025-03-01", "2025-03-03", "https://www.google.com", 1)
    assert repr(space) == '''Space(ID: None, Name: Buckingham Palace, Location: London, Description: It's a palace, Price: 45, Dates Available: {'2025-03-01': True, '2025-03-02': True, '2025-03-03': True}, Image: https://www.google.com, User_ID: 1)'''
