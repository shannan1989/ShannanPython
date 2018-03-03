#!/usr/bin/env python
#  coding=utf-8

import json
import os
import sys
import time
from multiprocessing import Pool  # 进程池

import config
import requests
from lxml import etree

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class TumblrSpider(object):
    proxies = {
        # "http": "http://127.0.0.1:56459",
        # "https": "http://127.0.0.1:56459",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
    }

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
                print(str(r.status_code) + ' ' + url)
                if r.status_code != 200:
                    continue
                else:
                    root = ET.fromstring(r.content)

                    tumblelog = root.find('tumblelog')
                    title = tumblelog.attrib.get('title')
                    if title is None:
                        title = tumblelog.attrib.get('name')

                    posts = root.find('posts')
                    total = min(50, (int)(posts.attrib.get('total')))

                    post_items = posts.findall('post')
                    post_items.reverse()
                    for post in post_items:
                        post_time = (float)(post.attrib.get('unix-timestamp'))

                        date = time.strftime("%Y-%m-%d", time.localtime(post_time))
                        dir_path = config.SavedPath + title + '/' + date
                        dir_ext = config.TumblrPath + title

                        for photo in post.iter('photo-url'):
                            if photo.attrib.get('max-width') == '1280':
                                self.save_image(photo.text, dir_path, dir_ext, post_time)

                        for c in post.findall('photo-caption'):
                            figures = etree.HTML(c.text).xpath("//figure[@class='tmblr-full']//img/@src")
                            for figure in figures:
                                self.save_image(figure, dir_path, dir_ext, post_time)

                        for c in post.findall('video-caption'):
                            figures = etree.HTML(c.text).xpath("//figure[@class='tmblr-full']//img/@src")
                            for figure in figures:
                                self.save_image(figure, dir_path, dir_ext, post_time)

                        for c in post.findall('regular-body'):
                            figures = etree.HTML(c.text).xpath("//figure[@class='tmblr-full']//img/@src")
                            for figure in figures:
                                self.save_image(figure, dir_path, dir_ext, post_time)

                        if self.setting['crawl_video'] is True:
                            for video in post.findall('video-player'):
                                if video.text is None:
                                    continue
                                video_options = etree.HTML(video.text).xpath("//video/@data-crt-options")
                                if len(video_options) <= 0:
                                    continue
                                data = json.loads(video_options[0])
                                if data['hdUrl'] is False:
                                    video_url = etree.HTML(video.text).xpath("//video//source/@src")[0]
                                else:
                                    video_url = data['hdUrl']

                                self.save_video(video_url, dir_path, dir_ext, post_time)

                time.sleep(5)

        except Exception as e:
            print('Exception occurs at line ' + e.__traceback__.tb_lineno.__str__(), e)

    def save_image(self, image_url, dir_path, dir_ext, post_time):
        ts = image_url.split('/')
        file_name = ts[len(ts) - 1]

        file_ext = '%s/%s' % (dir_ext, file_name)
        if os.path.exists(file_ext):
            os.utime(file_ext, (post_time, post_time))
            return

        if self.setting['crawl_all'] is False:
            if time.time() - post_time > 3600 * 8:
                return

        file_path = '%s/%s' % (dir_path, file_name)
        if os.path.exists(file_path):
            os.utime(file_path, (post_time, time.time()))
            return

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            print("Fetching " + image_url)
            ir = requests.get(image_url, proxies=self.proxies)
            if ir.status_code == 200:
                open(file_path, 'wb').write(ir.content)
                print("Saved to " + dir_path)
        except Exception as e:
            print("Save Photo Failed: ", e)

    def save_video(self, video_url, dir_path, dir_ext, post_time):
        ts = video_url.split('/')
        if 'tumblr_' in ts[len(ts) - 1]:
            file_name = ts[len(ts) - 1] + '.mp4'
        else:
            file_name = ts[len(ts) - 2] + '_' + ts[len(ts) - 1] + '.mp4'

        file_ext = '%s/%s' % (dir_ext, file_name)
        if os.path.exists(file_ext):
            os.utime(file_ext, (post_time, post_time))
            return

        if self.setting['crawl_all'] is False:
            if time.time() - post_time > 3600 * 8:
                return

        file_path = '%s/%s' % (dir_path, file_name)
        if os.path.exists(file_path):
            os.utime(file_path, (post_time, post_time))
            return

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            print("Fetching " + video_url)
            vr = requests.get(video_url, proxies=self.proxies)
            if vr.status_code == 200:
                open(file_path, 'wb').write(vr.content)
                print("Saved Video to " + file_path)
        except Exception as e:
            print("Save Video Failed: ", e)


def crawl(tumblr):
    spider = TumblrSpider(tumblr)
    spider.start()


def restart_spider():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def delete_empty_folder(_dir):
    if not os.path.isdir(_dir):
        return
    sub_files = os.listdir(_dir)
    for d in sub_files:
        delete_empty_folder(_dir + d + os.path.sep)
        if d == '.DS_Store':
            os.remove(_dir + d)
    if not os.listdir(_dir):
        os.rmdir(_dir)
        return


if __name__ == '__main__':
    print('Spider starts at ' + time.strftime("%Y-%m-%d %H:%M:%S"))
    start = time.time()

    pool = Pool(processes=len(config.Tumblrs))
    pool.map(crawl, config.Tumblrs)
    pool.close()
    pool.join()

    delete_empty_folder(config.SavedPath)

    end = time.time()
    print('Spider finishes, run %s seconds.' % (end - start))

    restart_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end + config.CrawlInterval))
    print('Spider will restart after %ss, at %s.' % (config.CrawlInterval, restart_time))
    time.sleep(config.CrawlInterval)
    restart_spider()
