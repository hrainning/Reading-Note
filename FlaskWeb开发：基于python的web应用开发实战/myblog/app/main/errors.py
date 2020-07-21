from flask import render_template
from . import main

#errorhandler只能在蓝本中触发，因此不 用
#注册程序全局的错误处理程序
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

#资源不可用
@main.app_errorhandler(403)
def forbidden(e):
    return