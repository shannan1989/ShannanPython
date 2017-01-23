# coding=utf-8

import os
import re
import time
from multiprocessing.dummy import Pool

import requests
from lxml import etree


class UgirlsSpider(object):
    save_path = "/Photo/Crawl/Ugirls/"
    proxies = {
        # "http": "http://127.0.0.1:56459",
        # "https": "http://127.0.0.1:56459",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
    }
    start_url = "http://www.meitulu.com/t/aiyouwu/"

    def start(self):
        self.parse(self.start_url)

    def parse(self, url):
        r = requests.get(url, allow_redirects=True, proxies=self.proxies, headers=self.headers)
        print str(r.status_code) + ' ' + url
        if r.status_code != 200:
            return
        else:
            try:
                html = etree.HTML(r.content)

                # 获取下一页
                exp = u'//div[@id="pages"]//a[text()="下一页"]/@href'
                next_page = html.xpath(exp)[0]
                if next_page != url:
                    # self.parse(next_page)
                    pass

                # 获取列表
                items = html.xpath("//p[@class='p_title']//a/@href")
                pool = Pool(processes=5)
                pool.map(self.parse_item, items)
                pool.close()
                pool.join()

            except Exception, e:
                print e.message

    def parse_item(self, url):
        r = requests.get(url, allow_redirects=True, proxies=self.proxies, headers=self.headers)
        print str(r.status_code) + ' ' + url
        if r.status_code != 200:
            return
        else:
            try:
                html = etree.HTML(r.content)

                # 保存图片
                name = html.xpath("//title")[0].text
                name = name.split("_")[0]
                name = re.sub(u"(?isu)_美图录", u"", name)
                name = re.sub(u"\[爱尤物\](?isu)", u"[Ugirls]", name)
                name = re.sub(u"\[Ugirls爱尤物\](?isu)", u"[Ugirls]", name)
                dir_path = self.save_path + name
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                images = html.xpath("//div[@class='content']//center//img/@src")
                for image_url in images:
                    ts = image_url.split('/')
                    file_name = ts[len(ts) - 1]
                    file_path = '%s/%s' % (dir_path, file_name)
                    if os.path.exists(file_path):
                        continue

                    print "Fetching " + image_url
                    try:
                        ir = requests.get(image_url, proxies=self.proxies, timeout=10)
                        if ir.status_code == 200:
                            open(file_path, 'wb').write(ir.content)
                            print "Saved to " + file_path
                    except Exception, e:
                        print "Save Failed: " + str(e.message)

                # 获取下一页图片
                exp = u'//div[@id="pages"]//a[text()="下一页"]/@href'
                next_page = html.xpath(exp)[0]
                if next_page != url:
                    self.parse_item(next_page)

            except Exception, e:
                print e.message


if __name__ == '__main__':
    start = time.time()

spider = UgirlsSpider()
spider.start()
end = time.time()
print end - start
