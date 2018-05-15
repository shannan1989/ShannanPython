#!/usr/bin/env python
#  coding=utf-8

from .movie import Movie


class DoubanAPI(object):
    def __repr__(self):
        return '<Douban API>'

    @property
    def movie(self):
        return Movie()
