#!/usr/bin/env python

import json
import requests
import random


class ProxyInstance:
    def __init__(self, host, port):
        self.target_url = "http://ipinfo.ipidea.io"
        self.host = host
        self.port = port

    def valid(self):
        try:
            res = requests.get(
                self.target_url, proxies=self.proxies(), timeout=5)
            return res.status_code == 200
        except Exception as e:
            return False

    def proxies(self):
        proxies = {
            'http': 'http://{}:{}'.format(self.host, self.port),
            'https': 'http://{}:{}'.format(self.host, self.port),
        }
        return proxies


class Proxy:
    def __init__(self, url):
        self.url = url
        self.proxies = list()

    def get_all_instances(self):
        try:
            resp = requests.get(url=self.url, timeout=5)
            if resp.status_code == 200:
                respData = json.loads(resp.text)
                for proxy in respData["data"]:
                    self.proxies.append(ProxyInstance(
                        proxy["ip"], proxy["port"]))
        except:
            pass

    def get_one_instance(self) -> ProxyInstance:
        if len(self.proxies) > 0:
            return random.choice(self.proxies)
        return None

    def get_one_proxy(self):
        instance = self.get_one_instance()
        if instance:
            return instance.proxies()
        return None
