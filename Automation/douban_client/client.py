# !/usr/bin/env python
#  coding=utf-8

from .api import DoubanAPI


class DoubanClient(DoubanAPI):
    def __repr__(self):
        return '<Douban Client>'
