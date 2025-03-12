from lib.booking import Booking
class BookingRepository():

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM bookings")
        bookings = []
        for row in rows:
            booking = Booking(row["id"], row['requested_dates'], row['user_id'], row['space_id'])
        return bookings

    def find(self, search_id: int):
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE id = %s", [search_id]
        )
        row = rows[0]
        booking = Booking.from_database(row["id"], row['requested_dates'], row['user_id'], row['space_id'])
        return booking
    
    def find_by_space(self, space_id: int):
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE space_id = %s", [space_id]
        )
        row = rows[0]
        booking = Booking.from_database(row["id"], row['requested_dates'], row['user_id'], row['space_id'])
        return booking

    def create(self, booking) -> None:
        self._connection.execute(
                "INSERT INTO bookings (requested_dates, user_id, space_id) VALUES (%s, %s, %s)",
                [booking.requested_dates, booking.user_id, booking.space_id],
            )

    def delete(self, booking_id: int) -> None:
        self._connection.execute("DELETE FROM bookings WHERE id = %s", [booking_id])
