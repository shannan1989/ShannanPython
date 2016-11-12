import urllib2

url = "http://www.shannanshuibei.net"
response = urllib2.urlopen(url)
print response.read()
print response.code