from celery import Celery
import requests
from bs4 import BeautifulSoup
from collections import ChainMap
import traceback
import sqlite3



app = Celery('tasks', broker='redis://127.0.0.1:6379//0',backend= 'redis://127.0.0.1:6379//1')#创建celery实例


@app.task
def start(url,key):
    conn = sqlite3.connect('77kpDB.db')#连接数据库
    headers = {
    'Connection' : 'keep-alive',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
}#伪装的请求头
    try:
        res = requests.get(url,headers,verify=False)#发送请求
        res.encoding = 'utf-8'#修改encoding，不然中文会显示乱码
        soup = BeautifulSoup(res.text,'lxml')
        item={}
        item['download']=soup.find_all('div','container')[5].find('a',class_='btn btn-sm btn-success').get('href')#下载链接
        item['name']=soup.find_all('div','container')[3].find('h3').text#电影名
        item2={soup.find_all('div','container')[4].find_all('div',class_='col-xs-4')[i].find('b').text:soup.find_all('div','container')[4].find_all('div',class_='col-xs-4')[i].find('span').text for i in range(0,6)}#其他信息
        item3 =ChainMap(item,item2)#合并两个字典
        try:#插入数据
            conn.execute('INSERT INTO magnet(id,title,filenum,url,activetime,hotindex,speed,creattime,file,key) \
         	VALUES(null,"{title}","{filenum}","{url}","{activetime}","{index}","{speed}","{creattime}","{file}","{key}")'.format(title=item3['name'],
                                                                                             filenum=item3['文件数量'],
                                                                                             creattime=item3['创建时间'],
                                                                                             activetime=item3['活跃时间'],
                                                                                             index=item3['热度指数'],
                                                                                             url=item3['download'],file=item3['文件大小'],speed=item3['连接速度'],key=key))
        except Exception:
            traceback.print_exc()
        print(item3)
        conn.commit()#提交数据库

    except Exception:
        traceback.print_exc()

