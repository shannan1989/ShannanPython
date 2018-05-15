#!/usr/bin/env python
#  coding=utf-8

from .base import DoubanBase


class Subject(DoubanBase):
    target = None

    def get(self, subject_id):
        return self._get('/v2/%s/subject/%s' % (self.target, subject_id))

    def search(self, q='', tag='', start=0, count=20):
        return self._get('/v2/%s/search' % self.target, q=q, tag=tag, start=start, count=count)
