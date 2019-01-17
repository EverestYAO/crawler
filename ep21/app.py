from pymongo import MongoClient
import sys
from flask import Flask, render_template
app = Flask(__name__)
class MGClient(object):
    def __init__(self):
        try:
            uri = "mongodb://127.0.0.1:27017/"
            self.c = MongoClient(uri)
        except Exception as e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
    def get_mongo_client(self, database="test"):#数据库test
        dbh = self.c[database]
        return dbh
db=MGClient().get_mongo_client().pic#连接mongodb，pic集合

@app.route('/<user>')
def hello_world(user):
    pic = [i['url'] for i in db.find({})]#从数据库读取url
    pic = ['https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1541234879076&di=dae2895f70e3742f22eddb27f2f79c4b&imgtype=0&src=http%3A%2F%2Fimg.bqatj.com%2Fimg%2F93659e88be128965.jpg',
           'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1541234940223&di=64f22bbdf03bd00ec496c611346c9496&imgtype=0&src=http%3A%2F%2Fku.90sjimg.com%2Felement_origin_min_pic%2F17%2F10%2F27%2F1b04ec179e0854a74fb4b8f6c1ca3cf2.jpg',
           'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1541234940223&di=a532f5e417fe670d1207bb21b161d48b&imgtype=0&src=http%3A%2F%2Fdmimg.5054399.com%2Fallimg%2Fqidai%2Fxmbqb%2F001.gif',]
    return render_template('test.html',user=user,number=pic)#传入模板

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)