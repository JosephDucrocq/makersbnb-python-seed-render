from lib.space import Space

class SpaceRepository():
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        spaces = []
        for row in rows:
            space = Space(row["id"], row['name'], row['location'], row['description'], row['availability'], row['price_per_night'], row['user_id'])
            spaces.append(space)
        return spaces
    
    def find(self, search_id: int):
        rows = self._connection.execute("SELECT * FROM spaces WHERE id = %s", [search_id])
        row = rows[0]
        space = Space(row["id"], row['name'], row['location'], row['description'], row['availability'], row['price_per_night'], row['user_id'])
        return space

    def create(self, space) -> None:
        self._connection.execute('INSERT INTO spaces (name, location, description, availability, price_per_night, user_id) VALUES(%s, %s, %s, %s, %s, %s)', [space.name, space.location, space.description, space.availability, space.price_per_night, space.user_id])

    def delete(self, space_id: int) -> None:
        self._connection.execute('DELETE FROM spaces WHERE id = %s', [space_id])

    