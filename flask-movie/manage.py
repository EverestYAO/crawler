from app import create_app
from flask_script import Manager
app = create_app('test')#创建app
manager = Manager(app)#使用flask-script管理项目运行

if __name__ == '__main__':
    manager.run()
