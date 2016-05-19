# -*- coding: utf-8 -*-

import json
import codecs
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import mysql.connector

def getConnection():
    config = {'host':'127.0.0.1',
          'user':'root',
          'password':'summer',
          'port':'3306',
          'database':'test',
          'charset':'utf8'
          }

    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    return cnn

class RaspspiderPipeline(object):
    def __init__(self):
        self.cnn = getConnection()
        self.cursor = self.cnn.cursor()

    def process_item(self, item, spider):

        tags = item['tags'][0]
        tt = ''
        for t in tags:
            tt = tt + t + ' '

        sql = "INSERT INTO raspberry(title,tags,date,img) VALUES (%s,%s,%s,%s)"


        data = (item['title'][0][0],tt[:-2],item['date'][0][0],item['img'][0])



        try:
            self.cursor.execute(sql,data)
            self.cnn.commit()
        except mysql.connector.Error as e:
            print(e)


        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnn.close()
        self.client.close()

class RaspImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item