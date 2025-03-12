from lib.space import Space
import json
class SpaceRepository():
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        spaces = []
        for row in rows:
            space = Space.from_database(row["id"], row['name'], row['location'], row['description'], row['price_per_night'], row['dates_available_dict'], row['image_content'], row['user_id'])
            spaces.append(space)
        return spaces
    
    def find(self, search_id: int):
        rows = self._connection.execute("SELECT * FROM spaces WHERE id = %s", [search_id])
        row = rows[0]
        space = Space.from_database(row["id"], row['name'], row['location'], row['description'], row['price_per_night'], row['dates_available_dict'], row['image_content'], row['user_id'])
        return space

    def create(self, space) -> None:
        dates_available_dict_json = json.dumps(space.dates_available_dict) # converting dictionary into json to then be inserted into database
        self._connection.execute('INSERT INTO spaces (name, location, description, price_per_night, dates_available_dict, image_content, user_id) VALUES(%s, %s, %s, %s, %s, %s, %s)', [space.name, space.location, space.description, space.price_per_night, str(dates_available_dict_json), space.image_content, space.user_id])

    def delete(self, space_id: int) -> None:
        self._connection.execute('DELETE FROM spaces WHERE id = %s', [space_id])

    