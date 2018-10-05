import os
basedir = os.path.abspath(os.path.dirname(__file__))#获取路径

class TestingConfig():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '77kpDB.db')#sqlite数据集所在位置


config = {
    'test': TestingConfig}#导入配置
 

   
