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
