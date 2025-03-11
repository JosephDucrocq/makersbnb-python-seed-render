class Space():
    def __init__(self, id: int, name: str, location: str, description: str, availability: bool, price_per_night: float, user_id: int) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.availability = availability
        self.price_per_night = price_per_night
        self.user_id = user_id

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Space(ID: {self.id}, Name: {self.name}, Location: {self.location}, Description: {self.description}, Availability: {self.availability}, Price: {self.price_per_night}, User_ID: {self.user_id})"
    
    def become_available(self):
        self.availability = True

    def become_unavailable(self):
        self.availability = False