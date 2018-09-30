import requests
import json
from bs4 import BeautifulSoup
import json
data = []
def start(offset=10):
    url = "https://mp.weixin.qq.com/mp/profile_ext"
    querystring = {"action": "getmsg", "__biz": "MzI0MDM0MzYwMA==", "f": ["json", "json"], "offset": "11",
                   "count": "10", "is_ok": "1", "scene": "124", "uin": "NDM3NzA2NDU=",
                   "key": "16b019ed9e0efa42b240862fa16812d26a06640e0bbc9de136316f5a4d60ca97e16d3b04c070d844b58d69d73ca7ef545fbbe89bcce96a6e1bdb1047546faf29e7ad0f87ea0e6afef11a8c0d2cb966c4",
                   "pass_ticket": "lyPH96T0uY4mp5mrK9JNCKEVTu4KTf1lyTr/zYUV5sQ=", "wxtoken": "",
                   "appmsg_token": "975_IqwiDuSDI5gUcuU4IB419kx_GbMG3Pbuyo7Jxw~~", "x5": "0"}

    headers = {
        'host': "mp.weixin.qq.com",
        'connection': "keep-alive",
        'accept': "*/*",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400",
        'x-requested-with': "XMLHttpRequest",
        'referer': "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI0MDM0MzYwMA==&scene=124&uin=NDM3NzA2NDU%3D&key=e73429b55c4357a911cebdb6f1cc6ef9c7ac0f07bb8cf709bfebef00e501e54107d989962c82c315e0a55a566969f0650810ceb6bedf488a9f1571abdcbe13eb8e781e4c2d643e4fb1346da822f18b24&devicetype=Windows+10&version=62060426&lang=zh_CN&a8scene=7&pass_ticket=lyPH96T0uY4mp5mrK9JNCKEVTu4KTf1lyTr%2FzYUV5sQ%3D&winzoom=1",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4",
        'cookie': "wxuin=43770645; devicetype=Windows10; version=62060426; lang=zh_CN; pass_ticket=lyPH96T0uY4mp5mrK9JNCKEVTu4KTf1lyTr/zYUV5sQ=; wap_sid2=CJXG7xQSXHF0Q0N6OVpqNGp6aFJiRjFLd3IwVXJoaUo3SVFwQmRORFYyZkhYZU8yNUtLOVZFWVV2d09QWURtX050NTJTRnZkYVFTN1ZCTU1JeVo5R1JlZ0ZaRGNjOERBQUF+MOmxkd0FOA1AlU4=",
        'cache-control': "no-cache",
        'postman-token': "1c24ef07-6b6e-1510-d996-714f3c9428ae"
    }

    response=requests.request("GET",url,headers=headers,params=querystring,verify=False).json( )
    print(response)
    for i in json.loads(response['general_msg_list'])['list']:
        link = i['app_msg_ext_info']['content_url']
        try:
            print(link)
            parse(link,headers)
        except Exception as e :
            print(e)
    if response['next_offset'] <100:
        start(response['next_offset'])
def parse(url,headers):
    response = requests.request("GET",url,headers=headers,verify=False).text
    #print(response)
    soup = BeautifulSoup(response,'lxml')
    #print(soup.find('h2',class_='rich_media_title'))
    #print(soup.find('em',id='publish_time'))
    title = soup.find('h2',class_='rich_media_title').get_text().strip()
    date = soup.find('em',id='publish_time').get_text().strip()
    content = soup.find('div',class_='rich_media_content').get_text().strip()
    item = {'title':title,
            'date':date,
            'content':content,
    }
    print(item)
    f = open('weixin.txt','a')
    f.writelines(json.dumps(item,ensure_ascii=False))
    f.close()
if __name__ == '__main__':
    start()