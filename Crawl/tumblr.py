# coding=utf-8

import os
import time

import requests
from lxml import etree


class TumblrSpider(object):
    start_urls = (
        'http://*.tumblr.com/api/read',
    )

    def parse(self):
        try:
            proxies = {
                "http": "http://127.0.0.1:56459",
                "https": "http://127.0.0.1:56459",
            }
            cookies = dict(logged_in='1')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
            }

            for start_url in self.start_urls:
                start = 0
                num = 50
                total = 100
                while start <= total:
                    url = start_url + '?num=' + str(num) + '&start=' + str(start)
                    start += num
                    r = requests.get(url, allow_redirects=False, proxies=proxies, headers=headers, cookies=cookies)
                    print str(r.status_code) + ' ' + url
                    if r.status_code != 200:
                        continue
                    else:
                        try:
                            html = etree.HTML(r.content)
                            title = html.xpath("//tumblelog/@title")[0]
                            total = (int)(html.xpath("//posts/@total")[0])
                            dir_path = '/Photo/Crawl/tumblr/' + title
                            if not os.path.exists(dir_path):
                                os.makedirs(dir_path)

                            images = html.xpath("//photo-url[@max-width='1280']")
                            for image in images:
                                image_url = image.text
                                ts = image_url.split('/')
                                file_name = ts[len(ts) - 1]
                                file_path = '%s/%s' % (dir_path, file_name)
                                if os.path.exists(file_path):
                                    continue

                                print image_url
                                print file_path
                                proxies = {
                                    "http": "http://127.0.0.1:56459",
                                    "https": "http://127.0.0.1:56459",
                                }
                                ir = requests.get(image_url, proxies=proxies)
                                if ir.status_code == 200:
                                    open(file_path, 'wb').write(ir.content)
                                pass
                        except Exception, e:
                            print e.message
                    pass

        except Exception, e:
            print e.message
        pass


if __name__ == '__main__':
    start = time.time()

spider = TumblrSpider()
spider.parse()
end = time.time()
print end - start
