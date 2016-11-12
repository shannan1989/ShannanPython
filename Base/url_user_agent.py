# coding=utf-8

# 某些网站反感爬虫的到访，于是对爬虫一律拒绝请求。所以用urllib2直接访问网站经常会出现HTTP Error 403: Forbidden的情况
# 对有些 header 要特别留意，Server 端会针对这些 header 做检查
# 1.User-Agent 有些 Server 或 Proxy 会检查该值，用来判断是否是浏览器发起的 Request
# 2.Content-Type 在使用 REST 接口时，Server 会检查该值，用来确定 HTTP Body 中的内容该怎样解析。

import urllib2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
request = urllib2.Request(url='http://www.baidu.com', headers=headers)
response = urllib2.urlopen(request)
print response.read()
print response.code
