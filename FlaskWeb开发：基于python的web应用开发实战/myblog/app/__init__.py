#flask对象
from flask import Flask

#命令行解析扩展
from flask_script import Manager
#提供用户界面的拓展
from flask_bootstrap import Bootstrap
#时间拓展
from flask_moment import Moment
from datetime import datetime
#生成表单，并验证提交的扩展
from flask_wtf import FlaskForm
#关系型数据库框架
from flask_sqlalchemy import SQLAlchemy
#数据迁移框架
from flask_migrate import Migrate,MigrateCommand
#登录管理扩展
from flask_login import LoginManager
#makrdown转化位html
from flask_pagedown import PageDown
#获取配置
from config import config


pagedown  =PageDown()
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()


#防止用户会话篡改
login_manager.session_protection = 'strong'
#登录界面端点函数,需要指定蓝本
login_manager.login_view = 'auth.login'

#工厂函数，延迟创建程序实例
def create_app(config_name):

    app = Flask(__name__)
    #使用app.config配置对象提供的from_object将配置导入程序中
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #拓展初始化
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 注册蓝本到程序上
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    from .auth import auth as auth_bulprint
    #注册时使用prefix使得所有路由都加上指定的前缀
    app.register_blueprint(auth_bulprint, url_prefix = '/auth')


    return app