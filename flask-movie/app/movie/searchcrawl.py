import asyncio
import re
import time
import traceback
from collections import ChainMap
from multiprocessing.dummy import Pool as ThreadPool

import requests
from bs4 import BeautifulSoup
import sqlite3
from .searchcrawl_task import start
conn = sqlite3.connect('77kpDB.db')
sql = """CREATE TABLE magnet( id INTEGER  PRIMARY KEY  autoincrement  ,title text,filenum INTEGER ,url text ,activetime text,hotindex text,speed text,creattime text,file text,key text)"""#建立字段
conn.execute('DROP TABLE IF EXISTS magnet')#如果存在table则删除
conn.execute(sql)#创建table
conn.commit()

headers = { 'user-agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'accept': "application/json",
    'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'accept-encoding': "gzip, deflate, br",
    'content-typ': "application/json"}
url_list=[]
data = []
def get_url( link):#进入列表页，爬取列表页里详情页的url
    #print(link)
    key = re.findall(r'kw-(.*?)-px',link)
    #print(key)
    res = requests.get(link, headers)#发送请求
    soup = BeautifulSoup(res.text, 'html.parser')#解析源代码
    for i in soup.find_all('div', class_='panel-body'):
        item = 'https://www.kkcili.com/' + i.find('a').get('href')#详情页url
        #print(item)
        start.delay(item,key[0])#爬取详情页


def crawl(name):#定义协程，搜索关键词
    url = 'https://www.kkcili.com/main-search-kw-%s-px-1-page-1.html' % name
    print(headers['user-agent'])
    res = requests.get(url, headers)#发送请求
    res.encoding = 'utf-8'#修改编码
    soup = BeautifulSoup(res.text, 'html.parser')#解析源代码
    # print(soup)
    # temp=soup.find('ul',class_='pagination col-md-8').find_all('li')[-1].find('a').get('href')
    page = re.findall(r'\d*',
                      soup.find('ul', class_='pagination col-md-8').find_all('li')[-1].find('a').get('href').split('-')[
                          -1])[0]  # 获取页数
    link_lis = ['https://www.kkcili.com/main-search-kw-%s-px-1-page-%s.html' % (name, str(i)) for i in
                range(1, int(page))[:2]]
    pool = ThreadPool(10)  # 进程池
    pool.map(get_url, link_lis)#从url列表映射到函数
    pool.close()
    pool.join()#直到任务完成关闭

# def start(url):
#     conn = sqlite3.connect('77kpDB.db')
#     headers = {
#     'Connection' : 'keep-alive',
#     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
# }
#     try:
#         res = requests.get(url,headers,verify=False)
#         res.encoding = 'utf-8'#修改encoding，不然中文会显示乱码
#         soup = BeautifulSoup(res.text,'lxml')
#         item={}
#         item['download']=soup.find_all('div','container')[5].find('a',class_='btn btn-sm btn-success').get('href')#下载链接
#         item['name']=soup.find_all('div','container')[3].find('h3').text#电影名
#         item2={soup.find_all('div','container')[4].find_all('div',class_='col-xs-4')[i].find('b').text:soup.find_all('div','container')[4].find_all('div',class_='col-xs-4')[i].find('span').text for i in range(0,6)}
#         item3 =ChainMap(item,item2)
#         try:#插入数据库
#             conn.execute('INSERT INTO magnet(id,title,filenum,url,activetime,hotindex,speed,creattime,file) \
#          	VALUES(null,"{title}","{filenum}","{url}","{activetime}","{index}","{speed}","{creattime}","{file}")'.format(title=item3['name'],
#                                                                                              filenum=item3['文件数量'],
#                                                                                              creattime=item3['创建时间'],
#                                                                                              activetime=item3['活跃时间'],
#                                                                                              index=item3['热度指数'],
#                                                                                              url=item3['download'],file=item3['文件大小'],speed=item3['连接速度']))
#         except Exception:
#             traceback.print_exc()
#         print(item3)
#         conn.commit()#提交到数据库
#
#     except Exception:
#         traceback.print_exc()


if __name__ == '__main__':
    start_time = time.time()
    crawl('吸血鬼日记')

    print(time.time()-start_time)

