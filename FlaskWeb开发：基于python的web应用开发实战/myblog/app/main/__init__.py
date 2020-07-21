#单脚本程序中，实例存在于全局中，路由可以直接修饰
#由于程序工厂函数，程序app实例只在运行时创建，必须先createapp之后才能定义路由
#使用蓝本，定义在蓝本中的路由处于休眠状态，直到蓝本注册到程序上时，路由才真正成为程序的一部分
#主要就是用来延迟路由作用的时间
from flask import Blueprint

#创建蓝本，蓝本名和所在的包或模块
main = Blueprint('main',__name__)

#放在末尾，避免循环导入依赖
from . import views, errors
from ..models import Permission

#白能量加入上下文处理器，使得能全局访问
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
