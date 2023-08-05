#!/usr/bin/env python

import requests as _requests
import pandas as pd


class Exchange:
    def __init__(self, session=None):
        self._session = session or _requests

    @property
    def session(self):
        return self._session

    def __str__(self):
        raise NotImplementedError()

    def to_df(self, proxy=None) -> pd.DataFrame:
        raise NotImplementedError()

    def to_json(self, proxy=None):
        return self.to_df(proxy).to_json()

    def to_csv(self, file, proxy=None):
        return self.to_df(proxy).to_csv(file)
