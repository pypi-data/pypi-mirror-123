#!/usr/bin/env python

from .exchange import Exchange
from .utils import user_agent
import pandas as pd


headers = {
    "Accept": "application/json, text/plain, */*",
    "DNT": "1",
    "Origin": "https://www.nasdaq.com",
    "Referer": "www.google.com",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": user_agent,
}


class Nasdaq(Exchange):
    """
    https://api.nasdaq.com/api/screener/stocks?tableonly=false&limit=0&offset=0&download=true
    """

    def __init__(self, session=None):
        super().__init__(session)
        self._base_url = "https://api.nasdaq.com/api/screener/stocks?"

    def __str__(self):
        return 'nasdaq'

    def _stocks(self, proxy=None):
        params = {
            'tableonly': 'false',
            'limit': 0,
            'offset': 0,
            'download': 'true',
        }
        data = self.session.get(
            url=self._base_url,
            params=params,
            proxies=proxy,
            headers=headers,
        )
        return data.json()

    def _dict_to_df(self, response) -> pd.DataFrame:
        try:
            rows = response.get('data').get(
                'table', response.get('data')).get('rows')
            table = pd.DataFrame(rows)
            return table
        except:
            return pd.DataFrame()

    def to_df(self, proxy=None) -> pd.DataFrame:
        return self._dict_to_df(self._stocks(proxy))
