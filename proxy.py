import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from pymongo import MongoClient
import redis

data=[]
db=MongoClient('127.0.0.1', 27017).test
def getIp(page):#爬取单页IP
    url='http://www.xicidaili.com/wt/%d'%(page)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    res = requests.get(url,headers=headers).text
    soup=BeautifulSoup(res,'lxml')
    for i in soup.find_all('tr'):
        try:
            data.append({'ip':'%s:%s'%(i.find_all('td')[1].get_text(),i.find_all('td')[2].get_text()),'verify':False})

        except:
            continue

pool = ThreadPool(10)
pool.map(getIp, [i for i in range(10)])#目标爬取页数，这里只爬取5页
pool.close()
pool.join()
db.ippool.insert_many(data)
print(len(data))
redispool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
r = redis.StrictRedis(connection_pool=redispool)
r.lpush('tq', 'action')