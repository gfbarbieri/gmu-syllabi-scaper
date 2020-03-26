import requests
from bs4 import BeautifulSoup

class Browser(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Chrome/74.0.3729.169'}

    def soupy_request(self, url, parameters):
        try:
            response = requests.get(url, headers=self.headers, params=parameters)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features='lxml')
        else
            soup = response.status_code

        return soup
