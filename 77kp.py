import requests
from bs4 import BeautifulSoup
def content(url):#影片主页
	res = requests.get(url)
	res.encoding='utf-8'
	res = res.text
	soup = BeautifulSoup(res,'lxml')
	download_url=soup.find_all('div',id='jishu')
	item = {}
	item['title'] = soup.find('h2').text#影片名
	item['cast'] =soup.find('div',class_='info fn-clear').find_all('dl')[0].text.strip()#主演
	item['story'] = soup.find('div',id='detail-intro').text.strip()#剧情简介
	item['chapter'] = []
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
			#item['chapter'].append(chapter)
	print(item)
def list_page(url):#列表页
	pass
def main_page(url):#主页
	pass

def run():#运行
	content('https://www.77kan.com/dongman/89097/')
run()
