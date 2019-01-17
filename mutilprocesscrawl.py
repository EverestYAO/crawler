import requests
import traceback
from multiprocessing import Process,Queue,Pool,Manager
from bs4 import BeautifulSoup
import threading
#伪装的请求头
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}
#列表函数
def list_page(url,q):
    print('start mission')
#发送请求并解析源码
    res=requests.get(url,headers=headers).text
    soup = BeautifulSoup(res,'lxml')
    audio=soup.find('div',class_='j-r-list').find('ul').find_all('li')
    alldata = []
#遍历获取音频文件名字和url写入队列中
    for i in audio:
        try:
            item=i.find('li',class_='j-r-list-tool-l-down f-tar j-down-video j-down-hide ipad-hide')
            if item:
                name=item.get('data-text')
                url=item.find('a').get('href'
                        )
                data={'name':name,'url':url}
                alldata.append(data)
#异常处理
        except Exception:
             traceback.print_exc()

    q.put(alldata)
            #print(i.find('a').get('href'))
#下载函数
def download_audio(item):
    name=item['name']
    url=item['url']
    res = requests.get(url,headers=headers)
    path = f'./audio/{name}.mp3'

#保存文件

    with open(path, 'wb') as f:

            f.write(res.content)

            f.close()

            print("文件保存成功")
def download(q):
    data=q.get(block=True)
    thread_list=[]
    for i in data:
        thread_list.append(threading.Thread(target=download_audio,args=[i]))
    for j in thread_list:
        j.start()
    for k in thread_list:
        k.join()
if __name__=='__main__':
    q=Queue()
    url='http://www.budejie.com/audio/'
    audio = 'http://mvoice.spriteapp.cn/voice/2016/0703/5778246106dab.mp3'
    t1= Process(target=list_page, args=(url,q)) 
    t1.start()
    t2= Process(target=download, args=(q,))
    t2.start()
    t1.join()
    t2.join()
    #download(audio)
