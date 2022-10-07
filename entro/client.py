import requests
import hashlib


class EntroClient:

    OBJECT_ID = "1"

    def __init__(self, url):
        self.url = url
        self.s = requests.Session()

    def login(self, username, password):
        # GET SALT AND SALT PASSWORD
        r = self.s.get(self.url + "/getvalue.cgi")

        values = self.parse_response(r.text)
        _type = values[1]
        salt = values[2]
        password_salted = hashlib.md5((salt + password).encode("utf-8")).hexdigest()

        # LOGIN
        r = self.s.get(
            self.url
            + "/login.cgi?id="
            + username
            + "&data="
            + password_salted
            + "&type="
            + _type
        )
        login_response = r.text.split("\t")
        self.session = login_response[2]

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
    def parse_response(data):
        values = data.split()
        return values
