import json
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
from pyecharts import GeoLines, Style#引入包
city= ['上海','北京','天津','南京','南宁','成都','武汉','杭州']
data_price=[]
def start(city):
    headers = { 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
    url = 'https://lp.flight.qunar.com/api/lp_calendar?dep=深圳&arr={city}&dep_date=2018-06-08&adultCount=1&month_lp=0&tax_incl=0&direct=0&callback=jsonp_77iruag5lhwjjw9'.format(city=city)#请求参数
    res = requests.get(url,headers=headers)
    print(city)
    for k in json.loads(re.findall(r'\{.*\}',res.text)[0])['data']['banner']:
        item={}
        if k['depDate'] == '2018-12-08':
            print(k['depDate'],' ',k['price'])
            item[city] = k['price']
            data_price.append(item)
pool = ThreadPool(10)
pool.map(start, city)#通过map将city列表里的元素逐一映射
pool.close()
pool.join()


style = Style(#一些基本的颜色长宽高的设定
    title_top="#fff",
    title_pos = "center",
    width=1200,
    height=600,
    background_color="#FFFFFF"
)
data_shenzhen = []

for i in data_price:
    if i[tuple(i.keys())[0]] <700:#如果价格小于700，则添加进一个数组
        item_shenzhen = ["深圳",tuple(i.keys())[0]]
        data_shenzhen.append(item_shenzhen)
style_geo = style.add(#地图的参数设置，包括图标，位置
    is_label_show=True,
    line_curve=0.2,
    line_opacity=0.6,
    legend_text_color="#eee",
    legend_pos="right",
    geo_effect_symbol="plane",#图标改成了飞机
    geo_effect_symbolsize=15,
    label_color=['#a6c84c', '#ffa022', '#46bee9'],
    label_pos="right",
    label_formatter="{b}",
    label_text_color="#eee",
)
geolines = GeoLines("GeoLines 示例", **style.init_style)
geolines.add("从深圳出发", data_shenzhen, **style_geo)
geolines.render(path='road.html')

from pyecharts import Bar#引入包
echart_city=[]#城市
echart_price=[]#价格
for p in data_price:#遍历数据，将城市和价格分开
    if p[tuple(p.keys())[0]]<700:
        echart_city.append(tuple(p.keys())[0])
        echart_price.append(p[tuple(p.keys())[0]])
bar = Bar("航班价格", "从深圳出发")#标题
bar.add("城市", echart_city,echart_price)#将城市、价格数据导入
bar.render(path='bar.html')#生成
