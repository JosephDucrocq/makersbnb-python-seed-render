from datetime import datetime, timedelta
class Booking:
    def __init__(self, id: int, start_date: str, end_date: str, user_id: int, space_id: int, approved: bool):
        self.id = id
        self.requested_dates = self.create_dates_requested_list(start_date, end_date)
        self.user_id = user_id
        self.space_id = space_id
        self.approved = approved

    def __repr__(self):
        return (
            f"Booking(ID: {self.id}, Requested Dates: {self.requested_dates}, Customer User ID: {self.user_id}, Space ID: {self.space_id}, Approved: {self.approved})"
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def create_dates_requested_list(self, start_date: datetime, end_date: datetime) -> dict:
            dates_requested_list = []
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            current_date = start_date
            while current_date <= end_date:
                dates_requested_list.append(str(current_date.date()))
                current_date += timedelta(days=1)
            return dates_requested_list

    @classmethod
    def from_database(cls, id: int, requested_dates: str, user_id: int, space_id: int, approved: bool):
        # Create a new instance
        instance = cls.__new__(cls)
        
        # Set attributes directly
        instance.id = id
        instance.requested_dates = requested_dates
        instance.user_id = user_id      
        instance.space_id = space_id
        instance.approved = approved      
        return instance