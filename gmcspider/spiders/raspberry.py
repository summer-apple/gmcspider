# -*- coding: utf-8 -*-
import scrapy
from gmcspider.items import RaspImgItem,RaspSpiderItem

class RaspberrySpider(scrapy.Spider):
    name = "raspberry"
    allowed_domains = ["shumeipai.nxez.com"]
    start_urls = (
        'http://shumeipai.nxez.com/',
    )
    # rules = (Rule(LinkExtractor(allow=('shumeipai.nxez\.com\/page', )), callback='parse'),)

    def parse(self, response):
        for article in response.css('article'):

            item = RaspSpiderItem()

            item['title']= article.css('.entry-title a::text').extract(),
            item['tags']= article.css('.tags-links a::text').extract(),
            item['date']= article.css('.entry-date::text').extract(),
            item['img']= article.css('.entry-content img::attr(src)').extract()


            yield item

        self.parse_img(response)


        nexturl = response.css('.nextpostslink::attr(href)').extract()[0]

        yield scrapy.Request(nexturl, callback=self.parse)


    def parse_img(self,response):
        img_item = RaspImgItem()
        img_item['image_urls'] = response.css('.entry-content img::attr(src)').extract()
        yield img_item

