# coding=utf-8

import os
import sys
import time
from multiprocessing.dummy import Pool

import requests
from lxml import etree

from config import *

reload(sys)
sys.setdefaultencoding("utf-8")


class VulgarSpider(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
    }
    categories = []

    def __init__(self, categories):
        self.categories = categories
        pass

    def start(self):
        count = len(self.categories)
        pool = Pool(processes=count)
        pool.map(self.parse, self.categories)
        pool.close()
        pool.join()

    def parse(self, cat):
        r = requests.get(cat['url'], allow_redirects=True, headers=self.headers)
        if r.status_code != 200:
            return
        else:
            try:
                html = etree.HTML(r.content)

                category = html.xpath("//div[@class='index_box']//h2//center")[0].text
                dir_path = SavedPath + category

                items = html.xpath("//div[@class='zxlist']//ul//li//a")
                new_items = []
                for item in items:
                    file_path = '%s/%s' % (dir_path, item.text + '.txt')
                    if os.path.exists(file_path):
                        continue

                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    new_item = {
                        'file_path': file_path,
                        'url': os.path.dirname(cat['url']) + item.attrib.get('href')
                    }
                    new_items.append(new_item)
                if len(new_items) > 0:
                    pool = Pool(processes=5)
                    pool.map(self.parse_item, new_items)
                    pool.close()
                    pool.join()

                try:
                    # 获取下一页
                    exp = u'//div[@class="page"]//a[text()=">>"]/@href'
                    current = (int)(html.xpath('//div[@class="page"]//span[@class="current"]/text()')[0])
                    if current < (int)(cat['crawl_page']):
                        next_page = os.path.dirname(cat['url']) + html.xpath(exp)[0]
                        if next_page != cat['url']:
                            self.parse({
                                'url': next_page,
                                'crawl_page': cat['crawl_page']
                            })
                except Exception:
                    pass

            except Exception, e:
                print('Error: ' + e.message)

    def parse_item(self, post):
        r = requests.get(post['url'], allow_redirects=False)
        if r.status_code != 200:
            return
        else:
            try:
                html = etree.HTML(r.content)

                print("Fetching " + post['url'])
                print('Saving to ' + post['file_path'])
                with open(post['file_path'], 'w') as f:
                    ttt = html.xpath("//div[@class='introtxt']//div[@class='n_bd']")[0]
                    nodes = ttt.xpath('node()')
                    for node in nodes:
                        if isinstance(node, etree._ElementUnicodeResult):
                            if node[0:2] == '　　':
                                f.write('\n')
                            f.write(node)

                        if isinstance(node, etree._Element):
                            if node.tag == 'p':
                                nodes2 = node.xpath('node()')
                                for node2 in nodes2:
                                    if isinstance(node2, etree._ElementUnicodeResult):
                                        node2 = node2.strip('\n')
                                        if node2[0:3] == '	　　':
                                            f.write('\n')
                                        f.write(node2)
                    print('Saved Novel to ' + post['file_path'])
            except Exception, e:
                print('Save Novel failed: ' + e.message)
                print(e.args)


def restart_spider():
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    print('Spider starts at ' + time.strftime("%Y-%m-%d %H:%M:%S"))
    start = time.time()

    spider = VulgarSpider(Categories)
    spider.start()

    end = time.time()
    print('Spider finishes, run %s seconds.' % (end - start))

    restart_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end + CrawlInterval))
    print('Spider will restart after %ss, at %s.' % (CrawlInterval, restart_time))
    time.sleep(CrawlInterval)
    restart_spider()
