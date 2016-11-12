# coding=utf-8

# requests是Python的一个HTTP客户端库，跟urllib，urllib2类似，那为什么要用requests而不用urllib2呢？
# 官方文档中是这样说明的：
# python的标准库urllib2提供了大部分需要的HTTP功能，但是API太逆天了，一个简单的功能就需要一大堆代码。
# 看requests的文档，确实很简单

import sys

import requests

reload(sys)
sys.setdefaultencoding('utf-8')

r = requests.get('https://api.github.com/user', auth=("user", 'pass'))
print r.status_code
print r.headers['content-type']
print r.encoding
print r.text
print r.json()
