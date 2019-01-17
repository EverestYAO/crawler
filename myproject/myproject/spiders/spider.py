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
            yield items
        
        self.log('A response from %s just arrived!' % response.url)

    def closed(self, reason):
        self.log("closed spider reason is %s" % reason)
        mailer = MailSender(
        smtphost = "smtp.aliyun.com",  # 发送邮件的服务器
        mailfrom = "zaojue405@aliyun.com",   # 邮件发送者
        smtpuser = "zaojue405@aliyun.com",   # 用户名
        smtppass = "pegasus405",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
        smtpport = 465   # 端口号
        )
        body = """
        发送的邮件内容
        """
        subject = '发送的邮件标题'
        # 如果说发送的内容太过简单的话，很可能会被当做垃圾邮件给禁止发送。
        mailer.send(to="58153287@qq.com", subject = subject, body = body)
