import requests
from bs4 import BeautifulSoup
import re
import redis
from multiprocessing.dummy import Pool as ThreadPool
import os
ip = '127.0.0.1'
password = ''
pool = redis.ConnectionPool(host=ip, port=6379, db=0, password=password)
r = redis.Redis(connection_pool=pool)
name=input('what movie do you want to see:')#输入想看的电影
headers = {
    'user-agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'accept': "application/json",
    'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'accept-encoding': "gzip, deflate, br",
    'content-typ': "application/json",
}
url='https://www.kkcili.com/main-search-kw-%s-px-1-page-1.html'%name
print(url)

res= requests.get(url,headers)
res.encoding='utf-8'
soup = BeautifulSoup(res.text,'html.parser')
#print(soup)
#temp=soup.find('ul',class_='pagination col-md-8').find_all('li')[-1].find('a').get('href')
page=re.findall(r'\d*',soup.find('ul',class_='pagination col-md-8').find_all('li')[-1].find('a').get('href').split('-')[-1])[0]#获取页数
link_lis=['https://www.kkcili.com/main-search-kw-%s-px-1-page-%s.html'%(name,str(i)) for i in range(1,int(page))]


def get_url(link):
    print(link)
    res = requests.get(link, headers)
    soup = BeautifulSoup(res.text,'html.parser')
    for i in soup.find_all('div',class_='panel-body'):
        item= 'https://www.kkcili.com/'+i.find('a').get('href')
        r.sadd('link',item)

pool = ThreadPool(10)
pool.map(get_url, link_lis)
pool.close()
pool.join()
os.system('python3 slave.py')

