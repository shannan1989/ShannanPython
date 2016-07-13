# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib2

from Meizitu import settings


class MeizituPipeline(object):
    def process_item(self, item, spider):
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)  # 存储路径
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        images = []
        for image_url in item['image_urls']:
            file_name = image_url.replace('http://pic.meizitu.com/wp-content/uploads/', '').replace('/', '')
            file_path = '%s/%s' % (dir_path, file_name)
            images.append(file_path)
            if os.path.exists(file_path):
                continue
            with open(file_path, 'wb') as file_writer:
                conn = urllib2.urlopen(image_url)  # 下载图片
                file_writer.write(conn.read())
            file_writer.close()
        item['images'] = images
        return item
