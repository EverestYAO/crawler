import requests
from bs4 import BeautifulSoup
import re
import redis
from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
from pymongo import MongoClient

print('-crawl name','\t\t\t\t\t想抓取的电影')
print('-check name key number','\t\t\t\t\t获取此电影的链接')
print ('参数列表:', str(sys.argv))
headers = { 'user-agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'accept': "application/json",
    'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'accept-encoding': "gzip, deflate, br",
    'content-typ': "application/json"}
class master(object):
    def __init__(self):
        self.ip = '127.0.0.1'
        self.password = ''
        self.pool = redis.ConnectionPool(host=self.ip, port=6379, db=0, password=self.password)
        self.r = redis.Redis(connection_pool=self.pool)
        self.name=name
        self.db=MongoClient('127.0.0.1', 27017).test


    def get_url(self,link):
        print(link)
        res = requests.get(link, self.headers)
        soup = BeautifulSoup(res.text,'html.parser')
        for i in soup.find_all('div',class_='panel-body'):
            item= 'https://www.kkcili.com/'+i.find('a').get('href')
            self.r.sadd('link',item)

    def crawl(self):
        url = 'https://www.kkcili.com/main-search-kw-%s-px-1-page-1.html' % name
        print(headers['user-agent'])
        res= requests.get(url,headers)
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text,'html.parser')
        #print(soup)
        #temp=soup.find('ul',class_='pagination col-md-8').find_all('li')[-1].find('a').get('href')
        page=re.findall(r'\d*',soup.find('ul',class_='pagination col-md-8').find_all('li')[-1].find('a').get('href').split('-')[-1])[0]#获取页数
        link_lis=['https://www.kkcili.com/main-search-kw-%s-px-1-page-%s.html'%(name,str(i)) for i in range(1,int(page))]

    def check(self,name,key,number):
        for i in self.db.movie.find({'name':{'$regex':"{name}.*{key}".format(name=name,key=key)},'连接速度':"很快"}).limit(number):
            print(i)



if 'crawl' in sys.argv[1] :
    print(sys.argv[2])
    name = sys.argv[2]
    print(name)
    master.crawl(name)#启动爬虫
elif 'check' in sys.argv[1]:
    name = sys.argv[2]
    key=''
    number=int(sys.argv[3])
    if len(sys.argv)>4:
        key = sys.argv[4]
    master().check(name,key,number)#查看数据库
