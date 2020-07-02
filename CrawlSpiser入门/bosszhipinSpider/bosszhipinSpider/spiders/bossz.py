# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import re

class BosszSpider(CrawlSpider):
    name = 'bossz'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=web&page=1&ka=page-1']

    data_link = LinkExtractor(allow=('.*?page=\d+.*?page-\d+'))
    rules = (
        Rule(data_link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # item = {}
        # #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # #item['name'] = response.xpath('//div[@id="name"]').get()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        xinxi = re.findall('span<.*?class="red">(.*?)</span>', response.text)
        print(xinxi)
