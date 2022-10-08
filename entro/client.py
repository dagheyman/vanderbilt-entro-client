import requests
import hashlib
from datetime import datetime, timezone, timedelta
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

    def login(self, username, password):
        r = self.s.get(self.url + "/getvalue.cgi")
        status, resp_values = self.parse_response(r.text)
        _type = resp_values[0]
        salt = resp_values[1]
        salted_pw = self.get_salted_pw(salt, password)

        r = self.s.get(
            self.url
            + "/login.cgi?id="
            + username
            + "&data="
            + salted_pw
            + "&type="
            + _type
        )
        status, resp_values = self.parse_response(r.text)
        self.session = resp_values[0]

    def get_active_booking(self):
        r = self.s.get(
            self.url
            + "/showres.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
            + "&type=0"
        )

        status, resp_values = self.parse_response(r.text)

        return Booking(
            title=resp_values[0],
            start=datetime.utcfromtimestamp(int(resp_values[1])),
            end=datetime.utcfromtimestamp(int(resp_values[4])),
        )

    def get_all_bookings():
        # TODO: It's the same API call above, but with type=1
        pass

    def make_booking(self, start, stop):
        r = self.s.get(
            self.url
            + "/makeres.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
            + "&start="
            + str(self.date_to_timestamp(start))
            + "&stop="
            + str(self.date_to_timestamp(stop))
        )
        status, resp_valies = self.parse_response(r.text)
        if status != "0":
            raise ValueError(status)

    @staticmethod
    def get_salted_pw(salt, password):
        return hashlib.md5((salt + password).encode("utf-8")).hexdigest()

    @staticmethod
    def parse_response(data):
        arr = data.split()
        return arr[0], arr[1:]

    @staticmethod
    def date_to_timestamp(date):
        return int(
            (date.replace(tzinfo=timezone.utc) - relativedelta(years=20)).timestamp()
        )

    def _debug(self):
        print("showres.cgi (my bookings)")
        r = self.s.get(
            self.url
            + "/showres.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
            + "&type=0"
        )
        print(r.text)

        print("showres.cgi (all bookings)")
        r = self.s.get(
            self.url
            + "/showres.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
            + "&type=1"
        )
        print(r.text)

        print("time.cgi")
        r = self.s.get(
            self.url + "/time.cgi?session=" + self.session + "&object=" + self.OBJECT_ID
        )
        print(r.text)

        print("combo.cgi")
        r = self.s.get(
            self.url
            + "/combo.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
        )  # need start and stop dates
        print(r.text)

        print("resdata.cgi")
        r = self.s.get(
            self.url
            + "/resdata.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
        )  # need start and stop dates and size
        print(r.text)
