class Space():
    def __init__(self, id: int, name: str, location: str, description: str, availability: bool, price: str, user_id: int) -> None:
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
        return f"Space({self.id}, {self.name}, {self.location}, {self.description}, {self.availability}, {self.price}, {self.user_id})"