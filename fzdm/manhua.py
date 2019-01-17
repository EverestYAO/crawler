
import aiohttp
import asyncio
import re
import hashlib
import os
import aiofiles
import logging
import shutil
import queue
from bs4 import BeautifulSoup
import traceback
import time


IMAGE_DIR = 'd:\\manka\\'
event = asyncio.Event()
AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'

HEADERS = {
    'User-Agent':AGENT
}


img_url = 'http://p1.xiaoshidi.net/'

url_list=[]
mh_list=[]

def check_image_dir_exist(DIR):
    """ 检查目录是否存在，存在则删除， 不存在则新建 """

    if  os.path.exists('d:\\manka\\%s' % DIR):
        shutil.rmtree('d:\\manka\\%s'%DIR)
    os.mkdir('d:\\manka\\%s' % DIR)

async  def get_img(q,url):
    async with aiohttp.ClientSession() as session:
            url = url+'index_{num}.html'
            for i in range(0,200):#默认一章漫画有200页，其实没有那么多
                try:
                    async  with session.get(url.format(num=i),headers=HEADERS) as resp:#发送请求
                        if resp.status == 200:#判断返回状态码，200为正常

                            content=await resp.read()
                            soup = BeautifulSoup(content,'lxml')#由于返回的源代码中文多为unicode，需要使用beautifulsoup进行解析
                            img_url = {'url':'http://p1.xiaoshidi.net/' + re.findall(r'mhurl="(.*?)"',str(content))[0],'page':str(i+1),
                                       'chapter':soup.find('div',id='weizhi').find_all('a')[-1].text.replace('讨论区',''),
                                       'name':soup.find('div',id='weizhi').find_all('a')[-2].text}#将单张漫画图片url和漫画章节写入字典
                            print(img_url)
                            await q.put(img_url)#将字典传入队列
                        else:#状态码不为200时断开，停止请求，一般为已经爬完当前章节所有页
                            break
                except Exception:
                    traceback.print_exc()
            event.set()

async def download(q):
    async with aiohttp.ClientSession() as session:#创建会话
        while 1:#开启死循环
            try:
                pic=  q.get_nowait()#从队列不等待获取元素

            except asyncio.QueueEmpty as e:#如果队列为空
                await asyncio.sleep(1)#等待一秒
                if event.is_set():#如果开启事件，退出循环
                    break
                continue


            async with session.get(pic['url'],headers=HEADERS) as resp:#发送请求
                try:
                    content = await resp.read()
                    check_image_dir_exist(pic['name']+'\\'+pic['chapter'])#检查存放漫画章节的文件夹是否建立
                    file_path = os.path.join(IMAGE_DIR, pic['name']+'\\'+pic['chapter']+'\\'+pic['page'] + '.jpg')#存放路径
                    async with aiofiles.open(file_path, 'wb+') as f:#写入文件
                        await f.write(content)
                        #logging.info(f'ok ... {file_path}... {now}')
                        q.task_done()#队列任务完成
                except Exception:
                    traceback.print_exc()
async def chapter(url):
    async with aiohttp.ClientSession() as session:#创建会话
        print(url)
        try:
            async  with session.get(url,headers=HEADERS) as resp:#发送请求
                if resp.status == 200:#状态码200为请求成功
                    content = await resp.read()
                    soup = BeautifulSoup(content, 'lxml')
                    print(soup.find('title').text.split(' ')[0])
                    manka_name = soup.find('title').text.split(' ')[0].replace('漫画','')
                    check_image_dir_exist(manka_name)#创建漫画目录
                    for i in soup.find('div',id='content').find_all('li'):#获取章节列表
                          url_list.append(url+i.find('a').get('href'))#获取章节url
        except Exception:
            traceback.print_exc()
            return None

async def manka():
    async with aiohttp.ClientSession() as session:  # 创建会话
        url = 'http://manhua.fzdm.com/'
        try:
            async  with session.get(url,headers=HEADERS) as resp:#发送请求
                if resp.status == 200:#状态码200为请求成功
                    content = await resp.read()
                    soup = BeautifulSoup(content, 'lxml')
                    for i in soup.find('div',id='mhmain').find_all('div',class_='round'):#获取漫画列表
                          mh_list.append('http://manhua.fzdm.com/'+i.find('a').get('href'))#拼接漫画url存在mh_list
                    print(mh_list)
        except Exception:
            traceback.print_exc()


                    
async def run(q,loop):
    manka_list = [asyncio.ensure_future(manka())]#建立漫画爬取任务
    await asyncio.wait(manka_list)#开启任务
    chapter_list=[asyncio.ensure_future(chapter(j) )for j in mh_list[4:5]]
    await asyncio.wait(chapter_list)
    tasks = [loop.create_task(get_img(q,i)) for i in url_list[500:700]]#建立章节爬取任务
    download_tasks= [loop.create_task(download(q)) for _ in range(5)]#开启下载队列
    await asyncio.wait(tasks + download_tasks)#任务合并运行

if __name__ == '__main__':
    start=time.time()
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(queue,loop))
    print(time.time()-start)