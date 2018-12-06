from . import db#通过__init__.py引入db

class Movie(db.Model):
    __tablename__= 'movie'#表明
    """ 建立字段并设置格式"""
    id = db.Column(db.Integer,primary_key = True)#id，自增，主键
    title = db.Column(db.Text)#标题 文本
    actor = db.Column(db.Text)#演员 文本
    body = db.Column(db.Text)#简介 文本
    pic = db.Column(db.Text)#图片url 文本
    url = db.Column(db.Text)#下载链接 文本
    movietype = db.Column(db.Text)#影片类型 文本

    def to_json(self):
        json_movie = {
            'actor': self.actor,
            'title':self.title,
            'body': self.body,
            'url': self.url,
            'pic':self.pic,
            'type':self.movietype}
        return json_movie

class Magnet(db.Model):
    __tablename__= 'magnet'#表名
    """ 建立字段并设置格式"""

    id = db.Column(db.Integer,primary_key = True)#id，自增，主键
    title = db.Column(db.Text)#标题 文本
    filenum = db.Column(db.Integer)#文件数量 整型
    activetime = db.Column(db.Text)#活跃时间 文本
    hotindex = db.Column(db.Text)#热度指数 文本
    url = db.Column(db.Text)#下载链接 文本
    speed = db.Column(db.Text)#速度 文本
    creattime = db.Column(db.Text)#创建时间 文本
    file = db.Column(db.Text)#文件大小 文本
    key = db.Column(db.Text)

