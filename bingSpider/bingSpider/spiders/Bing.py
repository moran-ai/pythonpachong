# -*- coding: utf-8 -*-
import scrapy


class BingSpider(scrapy.Spider):
    name = 'Bing'
    allowed_domains = ['cn.bing.com']
    start_urls = ['http://cn.bing.com/']

    def parse(self, response):
        pass
