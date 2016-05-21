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

        sql = "INSERT INTO raspberry(title,tags,date,img) VALUES (%s,%s,%s,%s)"

        data = (item['title'],item['tags'],item['date'],item['img'])



        try:
            self.cursor.execute(sql,data)
            self.cnn.commit()
        except mysql.connector.Error as e:
            print(e)


        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnn.close()
