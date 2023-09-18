# -*- coding: UTF-8 -*-
# 使用session进行持久化需要加该配置，一般20个字符左右
SECRET_KEY = 'asdzxcasdasdasdassss'
# 配置数据库信息
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'flask_project_01'

USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True   # 这里要使用ssl 加密
MAIL_USE_TLS = False
MAIL_DEBUG = True  # 开启debug 查看报错信息
MAIL_USERNAME = '1349814274@qq.com'
MAIL_PASSWORD = 'buikphjswvkxiahb'    # 授权码不能用空格
MAIL_DEFAULT_SENDER = '1349814274@qq.com'     #  默认的邮件发送者