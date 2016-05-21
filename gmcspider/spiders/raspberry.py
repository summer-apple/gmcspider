# -*- coding: utf-8 -*-
import scrapy
from gmcspider.items import RaspSpiderItem

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

            item['title']= article.css('.entry-title a::text').extract()[0]

            ts = article.css('.tags-links a::text').extract()
            tags = ''
            for t in ts:
                tags = tags+t+' '


            item['tags']= tags[:-1]

            item['date']= article.css('.entry-date::text').extract()[0]
            img = article.css('.entry-content img::attr(src)').extract()
            if len(img)==1:
                item['img'] = img[0]
            else:
                item['img'] = ''


            yield item


        nexturl = response.css('.nextpostslink::attr(href)').extract()[0]

        yield scrapy.Request(nexturl, callback=self.parse)

