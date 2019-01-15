import requests
import threading
import queue
from bs4 import BeautifulSoup
import time
import traceback
import json
#headers伪装的请求头
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}
#任务队列
workQueue = queue.Queue(400)
#存放列表页url的列表
link_list = []
def start(url):
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'lxml')
    pagetotal = int(soup.find_all('span',class_='page-numbers')[-1].text)
    for i in range(1,pagetotal+1):
        link = f'https://www.qiushibaike.com/8hr/page/{i}/'
        link_list.append(link)


def listpage(url):
    #发送请求
    res = requests.get(url=url,headers=headers)
    #解析源码
    soup = BeautifulSoup(res.text,'lxml')
    #遍历循环获取列表页中每一个详情页的标题和url
    for i in soup.find('div',class_='recommend-article').find('ul').find_all('li'):
        try:
            href = i.find('a').get('href')
            title = i.find('a').find('img').get('alt')
            link = f'https://www.qiushibaike.com{href}'
            item = {'title':title,'url':link}
            #将标题和url存放到队列中
            workQueue.put(item)
        except Exception:
            #当错误异常发生时，打印错误异常
            traceback.print_exc()
def save_file():
    #使用while开启无线循环，保持挂起状态
    while True:
        #从队列中获取任务，只使用get()方法。如果使用get_nowait()方法，队列为空的时候会抛异常
        item = workQueue.get()
        #以追加的模式，打开qiushibaike.txt
        f = open('qiushibaike.txt','a+')
        #写入内容
        f.writelines(json.dumps(item,ensure_ascii=False)+'\n')

#主入口url
url='https://www.qiushibaike.com/8hr/page/1/'
#启动start
start(url)
#多线程列表
thread_list = []
#遍历创建线程
for i in link_list:
    thread_item = threading.Thread(target=listpage,args=[i])
    thread_list.append(thread_item)
#单独将save_file线程加入到线程列表
thread_list.append(threading.Thread(target=save_file))
#遍历开启线程
for j in thread_list:
    j.start()
#遍历终结线程
for k in thread_list:
    k.join()


