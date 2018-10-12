import requests
from bs4 import BeautifulSoup
from collections import ChainMap
import redis
from multiprocessing.dummy import Pool as ThreadPool
from pymongo import MongoClient
import traceback
data=[]
def start(url):
    headers = {
    'Connection' : 'keep-alive',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
}
    try:
        res = requests.get(url,headers)
        res.encoding = 'utf-8'#修改encoding，不然中文会显示乱码
        soup = BeautifulSoup(res.text,'lxml')
        item={}
        item['download']=soup.find_all('div','container')[5].find('a',class_='btn btn-sm btn-success').get('href')#下载链接
        item['name']=soup.find_all('div','container')[3].find('h3').text#电影名
        item2={soup.find_all('div','container')[4].find_all('div',class_='col-xs-4')[i].find('b').text:soup.find_all('div','container')[4].find_all('div',class_='col-xs-4')[i].find('span').text for i in range(0,6)}
        item3 =ChainMap(item,item2)
        data.append(item3)
    except Exception:
        traceback.print_exc()
ip = '127.0.0.1'
password = ''
pool = redis.ConnectionPool(host=ip, port=6379, db=0, password=password)
r = redis.Redis(connection_pool=pool)#连接redis
url_lis=r.smembers('link')
print('start'.center(50,'='))
db=MongoClient('127.0.0.1', 27017).test
pool = ThreadPool(10)#进程池
pool.map(start, url_lis)
pool.close()
pool.join()
print(len(data))
db.movie.insert_many(data)
print('insert sucess'.center(50,'='))

