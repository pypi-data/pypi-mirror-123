# -*- coding: utf-8 -*-
import requests as _requests
import pandas as pd


nasdaq_headers = {
    "Accept": "application/json, text/plain, */*",
    "DNT": "1",
    "Origin": "https://www.nasdaq.com",
    "Referer": "www.google.com",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}


class Nasdaq():
    def __init__(self, session=None):
        self.session = session or _requests
        self._base_url = "https://api.nasdaq.com/api/screener/stocks?"

    def stocks(self, proxy=None):
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
            verify=False,
            headers=nasdaq_headers
        )
        return data.json()

    def dict_to_df(self, response) -> pd.DataFrame:
        try:
            rows = response.get('data').get('table').get('rows')
            table = pd.DataFrame(rows)
            return table
        except:
            return pd.DataFrame()
