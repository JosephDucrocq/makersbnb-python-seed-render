from datetime import datetime, timedelta
class Space():
    def __init__(self, id: int, name: str, location: str, description: str, price_per_night: float, start_date: str, end_date: str, image_content: str, user_id: int) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.price_per_night = price_per_night
        self.dates_available_dict = self.create_dates_availability_dict(start_date, end_date)
        self.image_content = image_content
        self.user_id = user_id

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Space(ID: {self.id}, Name: {self.name}, Location: {self.location}, Description: {self.description}, Price: {self.price_per_night}, Dates Available: {self.dates_available_dict}, Image: {self.image_content}, User_ID: {self.user_id})"
    
    def become_available(self):
        self.availability = True
        
    def become_unavailable(self):
        self.availability = False

    def create_dates_availability_dict(self, start_date: datetime, end_date: datetime) -> dict:
        dates_available_dict = {}
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        current_date = start_date
        while current_date <= end_date:
            dates_available_dict[str(current_date.date())] = True
            current_date += timedelta(days=1)
        return dates_available_dict
    

    @classmethod
    def from_database(cls, id: int, name: str, location: str, description: str, price_per_night: float, dates_available_dict: dict, image_content: str, user_id: int):
        # Create a new instance
        instance = cls.__new__(cls)
        
        # Set attributes directly
        instance.id = id
        instance.name = name
        instance.location = location        
        instance.description = description
        instance.price_per_night = price_per_night        
        instance.dates_available_dict = dates_available_dict
        instance.image_content = image_content        
        instance.user_id = user_id        
        return instance