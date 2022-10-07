import requests
import hashlib


class EntroClient:

    OBJECT_ID = "1"

    def __init__(self, url):
        self.url = url
        self.s = requests.Session()

    def login(self, username, password):
        r = self.s.get(self.url + "/getvalue.cgi")
        resp_values = self.parse_response(r.text)
        _type = resp_values[1]
        salt = resp_values[2]
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
        resp_values = self.parse_response(r.text)
        self.session = resp_values[1]

    def get_bookings(self):
        r = self.s.get(
            self.url
            + "/showres.cgi?session="
            + self.session
            + "&object="
            + self.OBJECT_ID
            + "&type=0"
        )
        print(r.text)

    @staticmethod
    def get_salted_pw(salt, password):
        return hashlib.md5((salt + password).encode("utf-8")).hexdigest()

    @staticmethod
    def parse_response(data):
        return data.split()
