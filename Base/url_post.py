import urllib
import urllib2

url = "http://www.baidu.com"
form = {
    'name': 'baidu',
    'type': 'sb'
}
form_data = urllib.urlencode(form)
request = urllib2.Request(url, form_data)
response = urllib2.urlopen(request)
print response.read()
print response.code
