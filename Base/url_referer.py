# coding=utf-8

import urllib2

headers = {
    'Referer': 'http://www.shannanshuibei.net'
}
request = urllib2.Request(url='http://www.baidu.com', headers=headers)
response = urllib2.urlopen(request)
print response.read()
print response.code
