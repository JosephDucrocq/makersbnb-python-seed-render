from lib.booking import Booking
import json


class BookingRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute(
            """
            SELECT * FROM bookings 
            ORDER BY id DESC
            """
        )
        bookings = []
        for row in rows:

            # Convert requested_dates from string to list if stored as JSON
            requested_dates = row["requested_dates"]
            if isinstance(requested_dates, str):
                try:
                    requested_dates = json.loads(requested_dates)
                except:
                    # If not valid JSON, keep as is (might be a plain string list)
                    pass

            booking = Booking.from_database(
                row["id"],
                row["user_id"],
                row["space_id"],
                row["requested_dates_list"],
                row.get("subtotal", 0),
                row.get("service_fee", 0),
                row.get("total", 0),
                row.get("approved", False),
            )
            bookings.append(booking)
        return bookings

    def find(self, search_id):
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE id = %s", [search_id]
        )
        if len(rows) == 0:
            return None

        row = rows[0]

        # Convert requested_dates from string to list if stored as JSON
        requested_dates_list = row["requested_dates_list"]
        if isinstance(requested_dates_list, str):
            try:
                requested_dates = json.loads(requested_dates)
            except:
                # If not valid JSON, keep as is (might be a plain string list)
                pass

        return Booking.from_database(
            row["id"],
            row["user_id"],
            row["space_id"],
            row["requested_dates_list"],
            row.get("subtotal", 0),
            row.get("service_fee", 0),
            row.get("total", 0),
            row.get("approved", False),
        )

    def find_by_space(self, space_id):
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE space_id = %s", [space_id]
        )
        bookings = []
        for row in rows:
            # Convert requested_dates from string to list if stored as JSON
            requested_dates = row["requested_dates"]
            if isinstance(requested_dates, str):
                try:
                    requested_dates = json.loads(requested_dates)
                except:
                    # If not valid JSON, keep as is
                    pass

            booking = Booking.from_database(
                row["id"],
                row["user_id"],
                row["space_id"],
                row["requested_dates_list"],
                row.get("subtotal", 0),
                row.get("service_fee", 0),
                row.get("total", 0),
                row.get("approved", False),
            )
            bookings.append(booking)
        return bookings

    def find_by_user(self, user_id):
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE user_id = %s ORDER BY id DESC", [user_id]
        )
        bookings = []
        for row in rows:
            # Convert requested_dates from string to list if stored as JSON
            requested_dates = row["requested_dates"]
            if isinstance(requested_dates, str):
                try:
                    requested_dates = json.loads(requested_dates)
                except:
                    # If not valid JSON, keep as is
                    pass

            booking = Booking.from_database(
                row["id"],
                row["user_id"],
                row["space_id"],
                row["requested_dates_list"],
                row.get("subtotal", 0),
                row.get("service_fee", 0),
                row.get("total", 0),
                row.get("approved", False),
            )
            bookings.append(booking)
        return bookings

    def create(self, booking):
        # Convert the requested_dates_list to JSON string for storage
        requested_dates_json = json.dumps(booking.requested_dates_list)

        rows = self._connection.execute(
            """
            INSERT INTO bookings 
            (user_id, space_id, requested_dates_list, 
            subtotal, service_fee, total, approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            [
                booking.user_id,
                booking.space_id,
                str(requested_dates_json),
                booking.subtotal,
                booking.service_fee,
                booking.total,
                booking.approved,
            ],
        )
        booking.id = rows[0]["id"]
        return booking

    def delete(self, booking_id):
        self._connection.execute("DELETE FROM bookings WHERE id = %s", [booking_id])

    def update_status(self, booking_id, new_status):
        self._connection.execute(
            "UPDATE bookings SET status = %s WHERE id = %s", [new_status, booking_id]
        )
