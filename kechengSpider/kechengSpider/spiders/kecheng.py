# -*- coding: utf-8 -*-
import scrapy
from kechengSpider.items import KechengspiderItem
from bs4 import BeautifulSoup

class KechengSpider(scrapy.Spider):
    name = 'kecheng'
    allowed_domains = ['imooc.com']
    # start_urls = ['http://imooc.com/']

    # start_urls = []
    # for page in range(0, 2):
    #     url = 'http://www.imooc.com/course/list?page={}'.format(page + 1)
    #     start_urls.append(url)
    start_urls = ['http://www.imooc.com/course/list?page={}'.format(i) for i in range(1, int(input("请输入需要获取的页数：")) + 1)]

    def parse(self, response):
        for data in response.xpath("//div[@class='course-list']/div[@class='moco-course-list']/div[@class='clearfix']"):
            item = KechengspiderItem()
            urls = data.xpath(".//@data-original").getall()
            for url_ in urls:
                # url
                url = 'http:' + url_

                # 标题
                title = data.xpath(".//h3/text()").getall()
                print(title)
                # 课程介绍
                free = data.xpath(".//div[@class='clearfix course-card-bottom']/p[@class='course-card-desc']/text()").getall()
                print(free)
                # 观看人数
                num_vis = data.xpath(".//div[@class='course-card-info']/span[2]/text()").getall()

                # item['url'] = url
                # item['title'] = title
                # item['free'] = free
                # item['num_vis'] = num_vis
                # yield item


"""
    def parse(self, response):
        item = KechengspiderItem()
        soup = BeautifulSoup(response.text, 'lxml')
        list = soup.select('div.course-card-container')
        for elem in list:
            item['title'] = elem.find('h3', class_='course-card-name').text
            item['free'] = 'http://www.imooc.com/' + elem.find('a', class_='course-card').attrs['href']
            item['url'] = 'http:' + elem.select('div.course-card-top img')[0].attrs['data-original']
            print(item)
            # yield item
"""



