import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from multiprocessing.dummy import Pool as ThreadPool
import traceback


conn = sqlite3.connect('77kpDB.db')

sql = """CREATE TABLE movie( id INTEGER  PRIMARY KEY  autoincrement  ,title text,actor text ,url text ,body text, pic text,movietype text)"""#建立字段
conn.execute('DROP TABLE IF EXISTS movie')#如果存在table则删除
conn.execute(sql)#创建table


def content(url):#影片主页
	conn = sqlite3.connect('77kpDB.db')
	headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
	res = requests.get(url,headers=headers)
	res.encoding='utf-8'
	res = res.text
	soup = BeautifulSoup(res,'lxml')
	download_url=soup.find_all('div',id='jishu')
	item = {}
	item['title'] = soup.find('h2').text#影片名
	item['type'] = soup.find('div',class_='position w960 fn-clear').find('div',class_='fn-left').find_all('a')[-2].text
	print(item['type'])
	item['cast'] =soup.find('div',class_='info fn-clear').find_all('dl')[0].text.strip()#主演
	item['story'] = soup.find('div',id='detail-intro').text.strip()#剧情简介
	item['chapter'] = []
	item['pic'] = 'https:'+soup.find('div',class_='detail-pic fn-left').find('img').get('src')
	print(item['title'])
	print(item['cast'])
	print(item['story'].strip())
	for i in download_url:
		for j in i.find_all('li'):
			print(j.find('a').get('title'))
			chapter={}
			chapter['title'] = j.find('a').get('title')#对应的集数
			print(j.find('a').get('href'))
			chapter['url'] = j.find('a').get('href')#下载url
			if 'magnet' in chapter['url']:#分类，磁力链接
				chapter['type'] = 'magnet'
			elif 'thunder' in chapter['url']:#分类，迅雷链接
				chapter['type'] = 'thunder'
			item['chapter'].append(chapter)
	print(item)
	try:
		conn.execute('INSERT INTO movie(id,title,actor,body,pic,url,movietype) \
	 	VALUES(null,"{title}","{actor}","{body}","{pic}","{url}","{movietype}")'.format(title=item['title'],actor=item['cast'],movietype=item['type'],body=item['story'],pic=item['pic'],url=item['chapter']))
	except Exception:
		traceback.print_exc()
		print('faild')
	conn.commit()

def list_page_thread(url):
	print(url.center(50,'*'))
	headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}#伪装的请求头
	res = requests.get(url=url,headers=headers)#发送请求
	res.encoding = 'utf-8'#修改编码为utf8
	res = res.text#获取源码文本
	soup = BeautifulSoup(res,'lxml')#解析源码
	for i in soup.find('ul',id='contents').find_all('li'):#获取当前页码内所有电影详情页url
		content_url = 'https://www.77kan.com' + i.find('a').get('href')#拼接生成url
		print(content_url)
		content(content_url)#调用content方法，爬取详情页
def list_page(url):#列表页
	headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}#伪装的请求头
	res = requests.get(url=url,headers=headers)#发送请求
	res.encoding = 'utf-8'#修改编码
	res = res.text#获取文本
	soup = BeautifulSoup(res,'lxml')#解析源码
	pagenum = soup.find_all('div',class_='pages')[-1].find_all('a')[-1].get('href')#获取页码（未清洗）
	pagenum = re.findall(r'\d{1,3}',pagenum.split('pg')[-1])[0]#获取页码（清洗提取数字，数据类型为字符串）
	print(pagenum)
	print(url.split('pg')[0]+'pg-%s.html'%str(pagenum))
	list_url_list = [ url.split('pg')[0]+'pg-%s.html'%str(i) for i in range(1,int(pagenum)+1)]#列表推导式，生成所有列表页的url
	pool = ThreadPool(2)#多进程，太快的话会被封禁，用2个进程比较安全
	pool.map(list_page_thread,list_url_list[:2])#通过映射的方式，调用函数
	pool.close()
	pool.join()#堵塞直到任务完成
def main_page(url):#主页
	headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}#伪装的请求头
	res = requests.get(url=url,headers=headers)#发送请求
	res.encoding = 'utf-8'#修改编码
	res = res.text#获取文本
	soup = BeautifulSoup(res,'lxml')#解析源码
	type_url_list = soup.find('div',class_='index-tags fn-clear').find_all('a')#类别url集合
	for i in type_url_list:
		list_url='https://www.77kan.com'+i.get('href')#拼接完整的电影类别url
		list_page(list_url)#调用list_page方法
def run():#运行
	list_page('https://www.77kan.com/vod-type-id-14-pg-1.html')#抓取指定类
	#content('https://www.77kan.com/dongman/89097/')#抓取指定某部电影
	#main_page('https://www.77kan.com/')#全站抓取

run()
