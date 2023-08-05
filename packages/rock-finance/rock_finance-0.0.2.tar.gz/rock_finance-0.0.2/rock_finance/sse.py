#!/usr/bin/env python

from .exchange import Exchange
from .utils import user_agent
import pandas as pd
from io import StringIO


headers = {
    "Host": "query.sse.com.cn",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Origin": "http://www.sse.com.cn",
    "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
    "Accept-Encoding": "gzip:deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": user_agent,
}


class SSE(Exchange):
    """
    http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1
    """

    def __init__(self, session=None):
        super().__init__(session)
        self._base_url = "http://query.sse.com.cn/security/stock/downloadStockListFile.do?"

    def _stock_type(self):
        raise NotImplementedError()

    def _params(self):
        return {
            "csrcCode": "",
            "stockCode": "",
            "areaName": "",
            "stockType": self._stock_type(),
        }

    def __str__(self):
        raise NotImplementedError()

    def to_df(self, proxy=None) -> pd.DataFrame:
        r = self.session.get(
            url=self._base_url,
            params=self._params(),
            proxies=proxy,
            headers=headers,
        )
        return pd.read_csv(StringIO(r.content.decode('gb18030')), sep='\t')


class SSE1(SSE):
    """
    A股
    """
    def __init__(self, session=None):
        super().__init__(session)

    def _stock_type(self):
        return "1"

    def __str__(self):
        return 'sse1'


class SSE2(SSE):
    """
    B股
    """
    def __init__(self, session=None):
        super().__init__(session)

    def _stock_type(self):
        return "2"

    def __str__(self):
        return 'sse2'


class SSE8(SSE):
    """
    科创板
    """
    def __init__(self, session=None):
        super().__init__(session)

    def _stock_type(self):
        return "8"

    def __str__(self):
        return 'sse8'
