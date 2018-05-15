#!/usr/bin/env python
#  coding=utf-8

import requests
from fake_useragent import UserAgent


class DoubanBase(object):
    API_HOST = 'https://api.douban.com'
    headers = {}

    def __repr__(self):
        return '<Douban Base>'

    def _get(self, uri, **opts):
        url = self.API_HOST + uri
        ua = UserAgent()
        self.headers['User-Agent'] = ua.random
        r = requests.get(url, params=opts, allow_redirects=True, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(str(r.status_code) + ' ' + url)
            return None
