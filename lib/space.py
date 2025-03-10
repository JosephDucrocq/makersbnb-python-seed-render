class Space():
    def __init__(self, id: int, name: str, location: str, description: str, availability: bool, price: float, user_id: int) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.availability = availability
        self.price = price
        self.user_id = user_id

    def __eq__(self, other: Space) -> bool:
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Space(ID: {self.id}, Name: {self.name}, Location: {self.location}, Description: {self.description}, Availability: {self.availability}, Price: {self.price}, User_ID: {self.user_id})"