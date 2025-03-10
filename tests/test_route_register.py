"""
When: I go to makersbnb/register
Then: I should see the register page
"""
def test_register_get(db_connection, web_client):
    db_connection.seed('seeds/makers_bnb_Bowie.sql')
    response = web_client.get('/register')
    assert response.status_code == 200
    # did the page load??

"""
When: I register with my info 
Then: A new user object should be created and I should be logged in
"""
def test_register_post(db_connection, web_client):
    db_connection.seed('seeds/makers_bnb_Bowie.sql')
    response = web_client.post('/register', data={'text': 'username', 'text' : 'password'})
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'You have successfully registered"'
