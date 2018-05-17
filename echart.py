from pyecharts import GeoLines, Style
import json
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
# style = Style(
#     title_top="#fff",
#     title_pos = "center",
#     width=1200,
#     height=600,
#     background_color="#404a59"
# )
#
# data_guangzhou = [
#     ["广州", "上海"],
#     ["广州", "北京"],
#     ["广州", "南京"],
#     ["广州", "重庆"],
#     ["广州", "兰州"],
#     ["广州", "杭州"]
# ]
# style_geo = style.add(
#     is_label_show=True,
#     line_curve=0.2,
#     line_opacity=0.6,
#     legend_text_color="#eee",
#     legend_pos="right",
#     geo_effect_symbol="plane",
#     geo_effect_symbolsize=15,
#     label_color=['#a6c84c', '#ffa022', '#46bee9'],
#     label_pos="right",
#     label_formatter="{b}",
#     label_text_color="#eee",
# )
# geolines = GeoLines("GeoLines 示例", **style.init_style)
# geolines.add("从广州出发", data_guangzhou, **style_geo)
# geolines.render()

city = []
f = open('cities.json','rb')
data = json.loads(f.read().decode('utf-8'))
for i in data['provinces']:
    for j in i['citys']:
        city.append(j['citysName'])
print(len(city))
city2 = ['上海','北京','天津','南京','南宁']
def start(city):
    headers = { 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
    url = 'https://lp.flight.qunar.com/api/lp_calendar?dep=深圳&arr={city}&dep_date=2018-06-08&adultCount=1&month_lp=0&tax_incl=0&direct=0&callback=jsonp_77iruag5lhwjjw9'.format(city=city)
    res = requests.get(url,headers=headers)
    print(city)
    for k in json.loads(re.findall(r'\{.*\}',res.text)[0])['data']['banner']:
        item={}
        if k['depDate'] == '2018-06-08':
            print(k['depDate'],' ',k['price'])
            item[city] = k['price']


pool = ThreadPool(10)
pool.map(start, city2)
pool.close()
pool.join()




