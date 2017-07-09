# coding=utf-8

import ConfigParser
import json
import os
import time

import requests
from lxml import etree


class TumblrSpider(object):
    start_urls = ()
    crawl_all = False
    crawl_video = False

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('settings/tumblr.ini')
        for t in config.items("tumblrs"):
            self.start_urls += (t[1],)

    def parse(self):
        try:
            proxies = {
                "http": "http://127.0.0.1:56459",
                "https": "http://127.0.0.1:56459",
            }
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
                    r = requests.get(url, allow_redirects=True, proxies=proxies, headers=headers)
                    print str(r.status_code) + ' ' + url
                    if r.status_code != 200:
                        continue
                    else:
                        try:
                            html = etree.HTML(r.content)
                            try:
                                title = html.xpath("//tumblelog/@title")[0]
                            except Exception as e:
                                title = html.xpath("//tumblelog/@name")[0]

                            total = (int)(html.xpath("//posts/@total")[0])
                            dir_path = '/Photo/Crawl/Tumblr/' + title
                            dir_ext = '/Photo/Tumblr/' + title

                            images = html.xpath("//photo-url[@max-width='1280']")
                            for image in images:
                                image_url = image.text
                                ts = image_url.split('/')
                                file_name = ts[len(ts) - 1]
                                file_path = '%s/%s' % (dir_path, file_name)
                                if os.path.exists(file_path):
                                    continue

                                file_ext = '%s/%s' % (dir_ext, file_name)
                                if os.path.exists(file_ext):
                                    continue

                                if not os.path.exists(dir_path):
                                    os.makedirs(dir_path)

                                print "Fetching " + image_url
                                try:
                                    ir = requests.get(image_url, proxies=proxies)
                                    if ir.status_code == 200:
                                        open(file_path, 'wb').write(ir.content)
                                        print "Saved to " + file_path
                                except Exception, e:
                                    print "Save Failed: " + str(e.message)

                            if self.crawl_video is True:
                                videos = html.xpath("//video-player")
                                for video in videos:
                                    data = json.loads(etree.HTML(video.text).xpath("//video/@data-crt-options")[0])
                                    if data['hdUrl'] is False:
                                        continue
                                    ts = data['hdUrl'].split('/')
                                    file_name = ts[len(ts) - 2] + '_' + ts[len(ts) - 1] + '.mp4'
                                    file_path = '%s/%s' % (dir_path, file_name)
                                    if os.path.exists(file_path):
                                        continue
                                    print data['hdUrl']
                                    print file_path
                                    vr = requests.get(data['hdUrl'], proxies=proxies)
                                    if vr.status_code == 200:
                                        open(file_path, 'wb').write(vr.content)

                        except Exception, e:
                            print e.message

                    if self.crawl_all is False:
                        break

        except Exception, e:
            print e.message
        pass


if __name__ == '__main__':
    start = time.time()

spider = TumblrSpider()
spider.parse()
end = time.time()
print end - start
