from datetime import datetime, timedelta


class Booking:
    def __init__(
        self,
        id,
        start_date,
        end_date,
        user_id,
        space_id,
        subtotal=0,
        service_fee=0,
        total=0,
        status="confirmed",
    ):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.requested_dates = self.create_dates_requested_list(start_date, end_date)
        self.user_id = user_id
        self.space_id = space_id
        self.subtotal = subtotal
        self.service_fee = service_fee
        self.total = total
        self.status = status
        self.nights = self._calculate_nights()

    def __repr__(self):
        return (
            f"Booking(ID: {self.id}, Start: {self.start_date}, End: {self.end_date}, "
            f"Customer User ID: {self.user_id}, Space ID: {self.space_id}, "
            f"Total: {self.total})"
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def create_dates_requested_list(self, start_date, end_date):
        dates_requested_list = []
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        current_date = start_date
        while current_date <= end_date:
            dates_requested_list.append(str(current_date.date()))
            current_date += timedelta(days=1)
        return dates_requested_list

    def _calculate_nights(self):
        """Calculate the number of nights between start_date and end_date"""
        if not self.start_date or not self.end_date:
            return 0

        if isinstance(self.start_date, str):
            start = datetime.strptime(self.start_date, "%Y-%m-%d")
        else:
            start = self.start_date

        if isinstance(self.end_date, str):
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
        else:
            end = self.end_date

        delta = end - start
        return delta.days

    @classmethod
    def from_database(
        cls,
        id,
        requested_dates,
        user_id,
        space_id,
        start_date=None,
        end_date=None,
        subtotal=0,
        service_fee=0,
        total=0,
        status="confirmed",
    ):
        # Create a new instance
        instance = cls.__new__(cls)

        # Set attributes directly
        instance.id = id
        instance.requested_dates = requested_dates

        # If we have dates in the requested_dates list, use the first and last as start/end
        if isinstance(requested_dates, list) and len(requested_dates) > 0:
            instance.start_date = start_date or requested_dates[0]
            instance.end_date = end_date or requested_dates[-1]
        else:
            instance.start_date = start_date
            instance.end_date = end_date

        instance.user_id = user_id
        instance.space_id = space_id
        instance.subtotal = subtotal
        instance.service_fee = service_fee
        instance.total = total
        instance.status = status
        instance.nights = instance._calculate_nights()

        return instance
