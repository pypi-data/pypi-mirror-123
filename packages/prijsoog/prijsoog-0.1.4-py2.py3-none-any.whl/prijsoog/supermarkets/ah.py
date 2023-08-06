from prijsoog._base import PriceWatcher
from datetime import datetime
import time

class AhWatcher(PriceWatcher):
    """Albert Heijn price watcher."""

    def search(self, query: str):
        """Search different supermarkets for product query

        :param query: product name, e.g. 'appel'
        :type query: str
        :return: results of your search
        :rtype: dict
        """
        # Make sure there is at least 5 sec interval between requests.
        current_interval = datetime.now() - self.last_request
        if current_interval.seconds < self.min_delay:
            time.sleep(self.min_delay - current_interval.seconds)

        soup = super().make_request(f"https://www.ah.nl/zoeken?query={query}")

        # Css selector
        name_css = ".title_lineclamp__1dS7X"
        price_css = ".price_highlight__3B97G span"

        # Make selection
        selection = {
            "name": [name.contents[0] for name in soup.select(name_css)],
            "price": self._price_filter(soup.select(price_css)),
        }

        return dict(zip(*selection.values()))

    def _price_filter(self, prices):
        """Combine AH price elements '2', '.', '99' into '2.99'"""
        cleaned_prices = [price.contents[0] for price in prices]
        combined = [cleaned_prices[i : i + 3] for i in range(0, len(cleaned_prices), 3)]
        return [float("".join(price)) for price in combined]
