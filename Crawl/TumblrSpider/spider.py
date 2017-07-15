# coding=utf-8

import json
import os
import time
from multiprocessing import Pool

import requests
from lxml import etree

from config import *


class TumblrSpider(object):
    proxies = {
        "http": "http://127.0.0.1:56459",
        "https": "http://127.0.0.1:56459",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
    }
    setting = {}

    def __init__(self, tumblr):
        self.setting = tumblr

    def start(self):
        try:
            start = 0
            total = 10
            while start <= total:
                url = self.setting['url'] + '?num=' + str(self.setting['page_size']) + '&start=' + str(start)
                start += self.setting['page_size']
                r = requests.get(url, allow_redirects=True, proxies=self.proxies, headers=self.headers)
                print str(r.status_code) + ' ' + url
                if r.status_code != 200:
                    continue
                else:
                    html = etree.HTML(r.content)

                    total = (int)(html.xpath("//posts/@total")[0])

                    try:
                        title = html.xpath("//tumblelog/@title")[0]
                    except Exception as e:
                        title = html.xpath("//tumblelog/@name")[0]

                    dir_path = SavedPath + title
                    dir_ext = TumblrPath + title

                    images = html.xpath("//photo-url[@max-width='1280']")
                    for image in images:
                        image_url = image.text
                        ts = image_url.split('/')
                        file_name = ts[len(ts) - 1]

                        file_path = '%s/%s' % (dir_path, file_name)
                        if os.path.exists(file_path):
                            os.remove(file_path)

                        file_ext = '%s/%s' % (dir_ext, file_name)
                        if os.path.exists(file_ext):
                            continue

                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)

                        try:
                            print "Fetching " + image_url
                            ir = requests.get(image_url, proxies=self.proxies)
                            if ir.status_code == 200:
                                open(file_path, 'wb').write(ir.content)
                                print "Saved to " + dir_path
                        except Exception, e:
                            print "Save Failed: " + str(e.message)

                    if self.setting['crawl_video'] is True:
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

                            file_ext = '%s/%s' % (dir_ext, file_name)
                            if os.path.exists(file_ext):
                                continue

                            print "Fetching " + data['hdUrl']
                            vr = requests.get(data['hdUrl'], proxies=self.proxies)
                            if vr.status_code == 200:
                                open(file_path, 'wb').write(vr.content)
                                print "Saved to " + file_path

                if self.setting['crawl_all'] is False:
                    break
        except Exception, e:
            print e.message


def crawl(tumblr):
    spider = TumblrSpider(tumblr)
    spider.start()


if __name__ == '__main__':
    start = time.time()

    pool = Pool()
    pool.map(crawl, Tumblrs)
    pool.close()
    pool.join()

    end = time.time()
    print end - start
