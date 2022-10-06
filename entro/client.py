import requests
import hashlib

class EntroClient:

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def login(self, username, password):
        # GET SALT AND SALT PASSWORD
        r = self.session.get(self.url + '/getvalue.cgi')
        values = r.text.split('\t')
        salt = values[3]
        _type = values[2]
        password_salted = hashlib.md5((salt + password).encode('utf-8')).hexdigest()

        # LOGIN
        r = self.session.get(self.url + '/login.cgi?id=' + username + '&data=' + password_salted + '&type=' + _type)
        login_response = r.text.split('\t')
        session = login_response[2]

        print(r.text)
        print(r.status_code)
