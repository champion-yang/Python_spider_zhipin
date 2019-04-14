# -*- coding: utf-8 -*-
import scrapy
from bossZhipin.items import BosszhipinItem

class BossSpider(scrapy.Spider):
    # 这一块相当于初始化的函数，在调用的时候要加self  self.offset
    name = 'boss'
    allowed_domains = ['zhipin.com']

    offset = 0
    url = 'https://www.zhipin.com/c101010100-p100109/?page='
    start_urls = [ url + str(offset)]

    def parse(self, response):
        # 拿到所有的父类
        for each in response.xpath("//div[@class='job-primary']"):
            # 初始化模型对象  想象成一个字典
            item = BosszhipinItem()
            # 通过xpath返回一个选择器的列表，通过extract()转化为Unicode字符串，通过[0]取出列表中的唯一一个元素
            item['company'] = each.xpath("./div[@class='info-company']/div/h3/a/text()").extract()[0]
            item['position'] = each.xpath("./div[@class='info-primary']/h3/a/div[@class='job-title']/text()").extract()[0]
            item['wages'] = each.xpath("./div[@class='info-primary']/h3/a/span[@class]/text()").extract()[0]
            item['place'] = each.xpath("./div[@class='info-primary']/p/text()").extract()[0]
            item['experience'] = each.xpath("./div[@class='info-primary']/p/text()").extract()[1]
            # 将数据交给管道文件处理
            yield item
        # 重新发送请求  和引擎说有请求，引擎说你交给调度器-->调度器，入队列，出队列-->下载器去web服务器下载得到response文件-->response交给parse函数继续处理
        # 每次处理完一页的数据之后，重新发动下一页页面请求
        if self.offset < 10:
            self.offset += 1
        yield scrapy.Request(self.url + str(self.offset) , callback=self.parse)