
from flask import Flask,request,jsonify
import time
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
app.config['SECRET_KEY']='you-never-know'


def crawl():
    headers = {
            'cache-control': "no-cache",
	            'postman-token': "dd6b12bd-efbf-532a-475e-6568214bd3cb",
		            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
			        }
    url = 'https://www.qiushibaike.com/text/'
    res=requests.get(url=url,headers=headers).text
    soup = BeautifulSoup(res,'lxml')
    text=''
    for i in soup.find_all('div',class_='content'):
        text=text+i.text
    return text


@app.route('/qiubai',methods=['GET'])
def QIUBAI():
    #time.sleep(15)
    content=crawl()
    return 'finished'
if __name__ == '__main__':
    app.run(host=('0.0.0.0'),port=5000,debug=True)

