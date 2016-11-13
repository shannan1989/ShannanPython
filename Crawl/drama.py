# coding=utf-8

import sys
import time

import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')


class DramaSpider(object):
    start_urls = (
        'http://cn163.net/bbcjilu/',
        'http://cn163.net/bbk/',
        'http://cn163.net/new/',
        'http://cn163.net/ddc1/heme/',
        'http://cn163.net/ddc1/ddc2/',
        'http://cn163.net/ddc1/ddc3/',
        'http://cn163.net/ddc1/ddc5/',
        'http://cn163.net/ddc1/ddc6/',
        'http://cn163.net/ddc1/dko1/',
        'http://cn163.net/ddc1/season/',
    )

    def parse(self):
        try:
            for start_url in self.start_urls:
                page = 1
                while True:
                    url = start_url + 'page/' + str(page) + '/'
                    page += 1
                    r = requests.get(url, allow_redirects=True)
                    print str(r.status_code) + ' ' + url
                    if r.status_code != 200:
                        break
                    else:
                        html = etree.HTML(r.content)
                        posts = html.xpath("//div[@class='archive_title']//h2//a/@href")
                        for post in posts:
                            self.parse_item(post)
                        pass
                        pass
                    pass
                pass
        except Exception, e:
            print e.message
        pass

    def parse_item(self, post):
        r = requests.get(post, allow_redirects=False)
        print str(r.status_code) + ' ' + post
        if r.status_code != 200:
            return
        else:
            try:
                html = etree.HTML(r.content)
                name = html.xpath("//h2[@class='entry_title']")[0].text
                links = html.xpath("//div[@class='entry']//a/@href")
                with open('/shannan文档/dramas/' + name.replace('/', ' ') + '.txt', 'w') as f:
                    for link in links:
                        if link.find('ed2k') == -1 and link.find('magnet') == -1:
                            continue
                        f.write(link + '\n')
                    pass
                print 'Get links ... ', name, len(links)
            except Exception, e:
                print 'Save links failed: ' + e.message
                print e.args
            pass
        pass


if __name__ == '__main__':
    start = time.time()

spider = DramaSpider()
spider.parse()
end = time.time()
print end - start
