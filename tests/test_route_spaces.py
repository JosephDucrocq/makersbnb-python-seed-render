"""
When: I go to makersbnb/spaces
Then: I should see the spaces page
"""
def test_spaces_get(db_connection, web_client):
    db_connection.seed('seeds/makers_bnb_Bowie.sql')
    response = web_client.get('/spaces')
    assert response.status_code == 200
    # did the page load??