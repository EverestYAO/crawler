import scrapy

from myproject.items import MyprojectItem



class MySpider(scrapy.Spider):

#爬虫名

    name = 'qiushibaike'

#文字板块url

    start_urls = ['https://www.qiushibaike.com/text/']

#回调函数

def parse(self, response):

#通过xpath提取内容

        contents=response.selector.xpath("//div[@class='content']/span/text()").extract()

        #定义items作为数据暂存容器

        item= MyprojectItem()

        for i in contents:

            items['content'] = i.strip()

           #通过生成器yield将数据传送到pipeline进一步处理

            yield items

        self.log('A response from %s just arrived!' % response.url)

