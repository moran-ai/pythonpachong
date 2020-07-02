# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ctoSpider.items import CtospiderItem

class CtoSpider(scrapy.Spider):
    name = 'cto'
    allowed_domains = ['cto.com']
    start_urls = ['https://www.51cto.com/']

    def parse(self, response):
        with open('cto.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        items = []
        tree = etree.HTML(response.text)

        # 将获取的对象封装到items中
        item = CtospiderItem()

        # 名字
        name_xpath = "//div[@class='home-left-list'][1]/ul/li/div[@class='rinfo']/a/text()"
        name = tree.xpath(name_xpath)

        # 类型
        mold_xpath = "//div[@class='home-left-list'][1]/ul/li/div[@class='rinfo']/div[@class='time']/span/a[@class='tag'][1]/text()"
        mold = tree.xpath(mold_xpath)

        # 分类
        types_xpath = "//div[@class='home-left-list'][1]/ul/li/div[@class='rinfo']/div[@class='time']/span/a[@class='tag'][2]/text()"
        types = tree.xpath(types_xpath)

        # 构造数据
        item['name'] = name
        item['mold'] = mold
        item['types'] = types

        items.append(item)
        return items
