import requests
from bs4 import BeautifulSoup
import traceback
import os
import hashlib
import time

from pymongo import MongoClient
class MGClient(object):
    # def __new__(cls, *args, **kw):
    #     if not hasattr(cls, '_instance'):
    #         orig = super(MGClient, cls)
    #         cls._instance = orig.__new__(cls, *args, **kw)
    #     return cls._instance

    def __init__(self):
        try:
            #正式环境
            #uri = "mongodb://root:Scrapy123@dds-wz962ff5b9eb15941102.mongodb.rds.aliyuncs.com:3717,dds-wz962ff5b9eb15942349.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2406913"
            uri = "mongodb://127.0.0.1:27017/"
            #uri = "mongodb://readWriter:readWriter17@112.90.89.17:27017/"
            #uri = "mongodb://admin:silutiandi123@192.168.1.236:27017"
            self.c = MongoClient(uri)
        except Exception as e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)

    def get_mongo_client(self, database="test"):
        dbh = self.c[database]
        return dbh

db=MGClient().get_mongo_client().pic
url = 'https://www.gamersky.com/ent/201711/983208.shtml'
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


def list_page():
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}  # 伪装的请求头
    url = 'https://www.gamersky.com/ent/wp/'
    res = requests.get(url,headers=headers)#发送请求
    res.encoding='utf-8'#修改编码
    soup = BeautifulSoup(res.text,'lxml')
    for i in soup.find('ul',class_='pictxt contentpaging').find_all('li'):
        try:
            if not 'https' in i.find('div',class_='tit').find('a').get('href'):
               list_url= 'https://www.gamersky.com'+i.find('div',class_='tit').find('a').get('href')
               picture_page(list_url)#爬取图册
            else:
                list_url = i.find('div',class_='tit').find('a').get('href')
                picture_page(list_url)#爬取图册
        except Exception:#增加异常处理
            traceback.print_exc()

def picture_page(url):
    print(url)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}#伪装的请求头
    res = requests.get(url,headers=headers)#发送请求
    res.encoding='utf-8'#修改编码
    res=res.text#获取文本
    soup =BeautifulSoup(res,'lxml')#解析
    file = 'PC'#默认为PC文件夹
    for j in soup.find_all('p'):#遍历获取所有图片url
        try:
            #print(j.text)
            if '手机' in j.text:#如果字符串中有手机，则将文件夹改成PHONE
            #print(j.find('a').get('href'))
                file = 'PHONE'
            download_pic(j.find('img').get('src'), file)
        except Exception:#异常处理
            pass
            #traceback.print_exc()
    #print(soup)
    for i in soup.find('div',class_='page_css').find_all('a'):#找到下一页
        #print(i.text)
        if '下一页' in i.text:#如果从在下一页，递归，继续调用此方法
            #print(i)
            picture_page(i.get('href'))

def download_pic(url,file):#增加file入参
    if 'origin' not in url:
        #print(url.split('?')[-1])#获取正确的url地址
        db.insert({'url':url})
        #res = requests.get(url.split('?')[-1],headers=headers)
        #file_path = os.path.join('C:\\Users\\lenovo\\untitled\\gamerskypic\\%s'%file, url.split('origin')[-1])#图片保存路径，注意要提前先创建文件夹
        #print(file_path)
        #with open(file_path, 'wb+') as f:#保存图片
        #    f.write(res.content)
if __name__ == '__main__':
#picture_page(url)
   list_page()

#download_pic('http://www.gamersky.com/showimage/id_gamersky.shtml?http://img1.gamersky.com/image2017/11/20171125_zl_91_5/gamersky_08origin_15_201711251758629.jpg')