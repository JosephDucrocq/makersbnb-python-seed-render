"""
When: I go to makersbnb/register
Then: I should see the register page
"""
def test_register_get(db_connection, web_client):
    db_connection.seed('seeds/makers_bnb_Bowie.sql')
    response = web_client.get('/register')
    assert response.status_code == 200
    # did the page load??

