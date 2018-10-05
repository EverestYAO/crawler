from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)#创建应用
	app.config.from_object(config[config_name])#导入配置
	bootstrap.init_app(app)
	db.init_app(app)#初始化数据库
	from .movie import movie as movie_blueprint
	app.register_blueprint(movie_blueprint)#注册蓝图
	return app
	
