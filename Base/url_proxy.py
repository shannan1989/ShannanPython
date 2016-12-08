# coding=utf-8

import urllib2

# 在开发爬虫过程中经常会遇到IP被封掉的情况，这时就需要用到代理IP；
# 在urllib2包中有ProxyHandler类，通过此类可以设置代理访问网页

proxy_support = urllib2.ProxyHandler({'http': '127.0.0.1:56459'})
opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.baidu.com')
print response.read()
print response.code
