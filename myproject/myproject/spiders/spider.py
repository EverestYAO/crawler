import scrapy
from myproject.items import MyprojectItem
from scrapy.mail import MailSender
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
            yield scrapy.Request(url=items['image_urls'][0],callback=self.parse_image)
    def parse_image(self,response):
        self.log('这里是%s'%response.url)
        
        self.log('A response from %s just arrived!' % response.url)

    def closed(self, reason):
        self.log("closed spider reason is %s" % reason)
