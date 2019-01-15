import scrapy
from myproject.items import MyprojectItem

class MySpider(scrapy.Spider):
    name = 'qiushibaiketupian'
    #图片版块地址
    start_urls = ['https://www.qiushibaike.com/imgrank/']

    def parse(self, response):
        #通过xpath提取图片地址
        images=response.selector.xpath("//img[@class='illustration']/@src").extract()
        items= MyprojectItem()
        for i in images:
            #url写入到item中提交
            items['image_urls'] =['http:'+ i.strip()] 
            yield items
        
        self.log('A response from %s just arrived!' % response.url)
