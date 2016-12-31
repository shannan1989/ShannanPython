# -*- coding: utf-8 -*-
import logging
import os

import requests
import scrapy


class ComicsSpider(scrapy.Spider):
    name = "comics"
    allowed_domains = ["xeall.com"]
    start_urls = ()
    site_base = "http://www.xeall.com"

    def start_requests(self):
        urls = [
            "http://www.xeall.com/caihuatang/",
            "http://www.xeall.com/benzi",
            # "http://www.xeall.com/gongkou/",
            # "http://www.xeall.com/lifan/",
            # "http://www.xeall.com/shaonv/",
            # "http://www.xeall.com/shenshi/",
            # "http://www.xeall.com/guifu/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取漫画列表
        urls = response.xpath("//ul[@class='piclist listcon']//a[@class='pic show']/@href").extract()
        for url in urls:
            url = self.site_base + url
            yield scrapy.Request(url=url, callback=self.parse_comic)

        # 请求下一页
        exp = u'//ul[@class="pagelist"]//li//a[text()="下一页"]/@href'
        _next = response.xpath(exp).extract_first()
        if _next:
            next_page = os.path.join(os.path.dirname(response.url), _next)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_comic(self, response):
        # 保存图片
        comic_name = response.xpath("//li[@id='imgshow']//img/@alt").extract_first()
        img_url = response.xpath("//li[@id='imgshow']//img/@src").extract_first()
        img_num = response.xpath("//ul[@class='pagelist']//li[@class='thisclass']//a[@href='#']/text()").extract_first()
        self.parse_image(comic_name, img_url, img_num)

        # 请求下一页
        exp = u'//ul[@class="pagelist"]//li//a[text()="下一页"]/@href'
        _next = response.xpath(exp).extract_first()
        if _next:
            next_page = os.path.join(os.path.dirname(response.url), _next)
            yield scrapy.Request(next_page, callback=self.parse_comic)

    def parse_image(self, comic_name, img_url, img_num):
        dir_path = '/Photo/Crawl/Comic/' + comic_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_name = img_num + ".jpg"
        file_path = '%s/%s' % (dir_path, file_name)
        if os.path.exists(file_path):
            return

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            ir = requests.get(img_url, headers=headers)
            if ir.status_code == 200:
                open(file_path, 'wb').write(ir.content)
        except Exception, e:
            self.log(e.message, logging.ERROR)
