# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
from doubanSpider.items import DoubanspiderItem
import json

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    def start_requests(self):
        base_url = 'https://movie.douban.com/j/search_subjects?'
        data = {'type': 'movie', 'tag': '最新', 'page_limit': '20'}
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['page_start'] = page * 20
            url = base_url + urlencode(data)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for data in result["subjects"]:
            item = DoubanspiderItem()
            item['id'] = data['id']
            item['title'] = data['title']
            item['url'] = data['cover']
            item['rate'] = data['rate']
            yield item
