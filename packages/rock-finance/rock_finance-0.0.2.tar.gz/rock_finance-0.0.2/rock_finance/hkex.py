#!/usr/bin/env python

from .exchange import Exchange
import pandas as pd
import tempfile


class HKEX(Exchange):
    def __init__(self, session=None):
        super().__init__(session)
        self._url = "https://www.hkex.com.hk/chi/services/trading/securities/securitieslists/ListOfSecurities_c.xlsx"

    def __str__(self):
        return 'hkex'

    def to_df(self, proxy=None) -> pd.DataFrame:
        r = self.session.get(
            url=self._url,
            proxies=proxy
        )
        with tempfile.TemporaryFile() as f:
            f.write(r.content)
            return pd.read_excel(
                f,
                sheet_name='ListOfSecurities',
                skiprows=[0, 1],
                header=[2],
            )
