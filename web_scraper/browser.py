import requests
from bs4 import BeautifulSoup

class Browser(object):

    def __init__(self, headers={'User-Agent': 'Chrome/74.0.3729.169'}):
        self.headers = headers

    def request(self, url, parameters):
        try:
            response = requests.get(url, headers=self.headers, params=parameters)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return response

    def soup(self, response):
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features='lxml')
        else:
            soup = response.status_code

        return soup

    def download_html():
        pass
