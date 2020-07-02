# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
from dianshijuSpider.items import DianshijuspiderItem
import json

class DianshijuSpider(scrapy.Spider):
    name = 'dianshiju'
    allowed_domains = ['movie.douban.com']
    start_urls = []

    for i in range(1, int(input("请输入加载的次数："))+1):
        start_urls.append('https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}'.format(i*20))

    # def start_requests(self):
    #     base_url = 'https://movie.douban.com/j/search_subjects?'
    #     data = {
    #         'type': 'tv',
    #         'tag': '热门',
    #         'sort': 'recommend',
    #         'page_limit': '20'}
    #     for page in range(1, self.settings.get('MAX_PAGE')+1):
    #         data['page_start'] = page * 20
    #         url = base_url +

    def parse(self, response):
        json_data = json.loads(response.text)
        for data in json_data['subjects']:
            item = DianshijuspiderItem()
            item['url'] = data['cover']
            yield item