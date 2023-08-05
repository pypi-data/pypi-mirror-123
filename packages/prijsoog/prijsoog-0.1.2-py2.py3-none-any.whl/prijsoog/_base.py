"""Top-level package for Prijsoog."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime


CUSTOM_HEADER = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}


class PriceWatcher:
    """Main class that enables product & price retrieval of Dutch supermarkets"""

    def __init__(self, min_delay=5):
        """Class constructor

        :param min_delay: minimum request delay in sec
        :type min_delay: int
        """
        self.last_request = datetime(2000, 1, 1, 0, 0)
        self.min_delay = min_delay
        self.session = requests.Session()
        self.session.headers.update(CUSTOM_HEADER)

    def search(self, query: str) -> dict:
        """Search different supermarkets for product query

        :param query: product name, e.g. 'appel'
        :type query: str
        :return: results of your search
        :rtype: dict
        """
        pass

    def make_request(self, url):
        """Access website and parse data"""
        response = self.session.get(url)
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        return soup
