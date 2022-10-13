import requests
import hashlib
from typing import Tuple, List
from datetime import datetime, timezone
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta


@dataclass
class Booking:
    title: str
    start: datetime
    end: datetime


class EntroClient:

    OBJECT_ID = "1"

    def __init__(self, url):
        self.url = url
        self.s = requests.Session()

    def login(self, username, password) -> None:
        r = self.s.get(self.url + "/getvalue.cgi")
        status, resp_values = self.parse_response(r.text)
        _type = resp_values[0]
        salt = resp_values[1]
        salted_pw = self.get_salted_pw(salt, password)

        r = self.s.get(
            f"{self.url}/login.cgi?id={username}&data={salted_pw}&type={_type}"
        )
        status, resp_values = self.parse_response(r.text)
        self.session = resp_values[0]

    def get_active_booking(self) -> Booking:
        r = self.s.get(
            f"{self.url}/showres.cgi?session={self.session}&object={self.OBJECT_ID}&type=0"
        )

        status, resp_values = self.parse_response(r.text)

        return Booking(
            title=resp_values[0],
            start=datetime.utcfromtimestamp(int(resp_values[1])),
            end=datetime.utcfromtimestamp(int(resp_values[4])),
        )

    def get_all_bookings(self):
        # TODO: It's the same API call above, but with type=1
        pass

    def make_booking(self, start: datetime, stop: datetime) -> None:
        """
        Make a booking in the system. The start end stop time need to match with the pre-configured slots.

        Error codes:
                RESERVATION_OK              0
                RESERVATION_ERROR           1
                RESERVATION_INTERVAL_FULL   2
                RESERVATION_FAMILY_FULL     3
                RESERVATION_NO_TIME         4
                RESERVATION_PERIOD_FULL     5
                RESERVATION_OBJECT_DISABLED 6
        """
        start_timestamp = self.date_to_timestamp(start)
        stop_timestamp = self.date_to_timestamp(stop)
        r = self.s.get(
            f"{self.url}/makeres.cgi?session={self.session}&object={self.OBJECT_ID}&start={start_timestamp}&stop={stop_timestamp}"
        )
        status, resp_valies = self.parse_response(r.text)
        if status != "0":
            raise ValueError(status)

    @staticmethod
    def get_salted_pw(salt: str, password: str) -> str:
        return hashlib.md5((salt + password).encode("utf-8")).hexdigest()

    @staticmethod
    def parse_response(data: str) -> Tuple[str, List[str]]:
        arr = data.split()
        return arr[0], arr[1:]

    @staticmethod
    def date_to_timestamp(date: datetime) -> int:
        return int(
            (date.replace(tzinfo=timezone.utc) - relativedelta(years=20)).timestamp()
        )
