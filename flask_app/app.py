from flask import Flask, render_template
from pymongo import MongoClient

import os
class MGClient(object):
    # def __new__(cls, *args, **kw):
    #     if not hasattr(cls, '_instance'):
    #         orig = super(MGClient, cls)
    #         cls._instance = orig.__new__(cls, *args, **kw)
    #     return cls._instance

    def __init__(self):
        try:
            #正式环境
            #uri = "mongodb://root:Scrapy123@dds-wz962ff5b9eb15941102.mongodb.rds.aliyuncs.com:3717,dds-wz962ff5b9eb15942349.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2406913"
            uri = "mongodb://127.0.0.1:27017/"
            #uri = "mongodb://readWriter:readWriter17@112.90.89.17:27017/"
            #uri = "mongodb://admin:silutiandi123@192.168.1.236:27017"
            self.c = MongoClient(uri)
        except Exception as e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)

    def get_mongo_client(self, database="test"):
        dbh = self.c[database]
        return dbh

db=MGClient().get_mongo_client().pic


app = Flask(__name__)


@app.route('/<user>')
def hello_world(user):
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    print(request.path)
    print(request.args)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template("obj/test.html", index_list=index_list, html=html)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)