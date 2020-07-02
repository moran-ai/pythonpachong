# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
from baidutuSpider.items import BaidutuspiderItem
import json

class BaidutuSpider(scrapy.Spider):
    name = 'baidutu'
    allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com/']

    def start_requests(self):
        base_url = 'https://image.baidu.com/search/acjson?'
        data = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592',
        'is':'',
        'fp': 'result',
        'queryWord': '桥本有菜',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf - 8',
        'oe': 'utf - 8',
        'adpicid':'',
        'st': '-1',
        'z':'',
        'ic': '0',
        'hd':'',
        'latest':'',
        'copyright':'',
        'word': '桥本有菜',
        's':'',
        'se':'',
        'tab':'',
        'width':'',
        'height':'',
        'face': '0',
        'istype': '2',
        'qc':'',
        'nc': '1',
        'fr':'',
        'expermode':'',
        'force':'',
        'pn': '30',
        'rn': '30',
        'gsm': '1e',
        '1588655777338':''
        }
        for page in range(self.settings.get('MAX_PAGE')):
            url = base_url + urlencode(data)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.body)
        # print(result['data']['thumbURL'])
        for img in result['data']:
            item = BaidutuspiderItem()
            item['id'] = img['di']
            item['title'] = img['fromPageTitle'].replace('<strong>', '').replace('</strong>', '')
            item['url'] = img['middleURL']
            yield item
