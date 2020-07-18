## 材料

Flask 官方文档（http://flask.pocoo.org/）

源码： https://github.com/miguelgrinberg/flasky.git

## flask

优点：自由度高、支持的组件多，是一个可扩展的框架

组成：

- web服务器网关接口：wsgi
- 模板系统：jinja2

## 创建虚拟环境

windows:

1. 创建虚拟环境：python -m venv < dir >
2. 激活虚拟环境：venv\Scripts\activate 若要返回全局解释器用deactivate即可

ubuntu：

1. 安装virtualenv包：sudo apt-get install python-virtualenv
2. 创建虚拟环境：virtualenv venv
3. 激活虚拟环境：source venv/bin/activate

## 代码语法

代码必备结构：

1. flask实例
2. 路由+视图函数
3. run的启动代码

定义路由：Flask 使用app.route修饰器或者非修饰器形式的 app.add_url_rule() 生成路由映射

动态url：路由中用< var >来表示动态的路由，参数要写入视图函数，满足时作为变量调用

特殊路由：/static/< filename >  =》静态文件

视图函数：调用根据路由匹配，参数由url提供，返回值即是响应

## 路由定义

使用装饰器

- app.route(''/'')
- app.errorhandler(404)

## 视图函数返回值

- 通用参数：1页面内容、2状态码【默认200】、3header
- response响应对象：内容包括通用参数
- redirect重定向对象：指向地址由location首部提供
- abort错误对象：abort会把控制权转交给web服务器
- 渲染模板（render_template）html
- 

## 上下文

目的：让视图函数能访问一些对象用以处理请求

用from flask import xx导入，每个线程都有自己的上下文，使用前需要推送激活，而后就能使用这些上下文变量

程序上下文全局变量：

- current_app：当前激活程序的程序实例，激活方法用with app.content() : xx代码 来激活
- g： 处理请求时用作临时存储的对象。每次请求都会重设这个变量
- request：请求对象，封装了客户端发出的 HTTP 请求中的内容，request.form可以获得post中的表单数据
- session： 用户会话，用于存储请求之间需要“记住”的值，用字典的方式访问数据

## 钩子

作用：在视图函数调用前后调用某些注册通用函数

类型：

- before_first_request：注册一个函数，在处理第一个请求之前运行。 
- before_request：注册一个函数，在每次请求之前运行。
- after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
-  teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

钩子函数与视图数据共享：通过g

## flask实例对象app

属性：

- name：app的名字
- app_context：
- url_map：所有映射路由
- config：字典，来存储框架、扩展和程序本身的配置变量。

## flask函数

1、url_for函数：使用程序 URL 映射中保存 的信息生成 URL

1. 函数名 | static
2. 变量='xxx'，可以有多个
3. _external，生成绝对路径

2、flash函数：消息提示，但是需要在模板中用get_flashed_messages()显示

1. 消息提示的字符串

## 表单类

继承：Form [来源:flask.ext.wtf]

wtforms支持的字段见：https://wtforms.readthedocs.io/en/2.3.x/

## 状态码

- 200：请求成功处理
- 400：请求无效
- 302：重定向
- 404：客户端请求未知页面或路由
- 500：有未处理的异常

## 扩展

- flask-script：解析命令行，使用manager类控制
- flask-bootstrap：提供用户界面组件的开源框架，主要用在模板中
- [flask-moment](http://momentjs.com/docs/#/displaying/)：模板中渲染日期和时间
- [flask-wtf](https://flask-wtf.readthedocs.io/en/stable/)：处理web表单，每个表单都由一个继承自form的类表示。对[wtform](https://wtforms.readthedocs.io/en/2.3.x/)进行的包装，默认支持跨站请求伪造攻击CSRF保护
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)：抽象数据库集成框架，包装了了[SQLAlchemy](http://www.sqlalchemy.org/)框架
- [Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/)：用来做数据迁移，能跟踪数据库模式的变化，包装了[Alembic](https://alembic.readthedocs. org/en/latest/index.html)，并集成到flask-script中
- flask-mail：发送电子邮件，使用Message实现

一般使用方式：

```python
#使用xxx扩展
from flask.ext.xxx import xxx
app = Flask(__name__)
xxx = xxx(app)

app.run() #有时也可xxx.run()
```



## 模板

模板：是一个包含响应文本的文件，其中包含用占位变量表示的动态部分，其具体值只在请 求的上下文中才能知道。

渲染：使用真实值替换变量，再返回最终得到的响应字符串的过程。

渲染引擎：jinja2

path：默认情况下，Flask 在程序文件夹中的 templates 子文件夹中寻找模板。

渲染函数render_template参数：1模板、后边都是键值对参数

模板中的变量：

1. 表示方法：{{ var }}
2. 变量类型：几乎所有类型
3. 修改方式：过滤器，用竖线分割
4. 安全考量：jinja2默认转义所有变量

[变量过滤器]( https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters )

- safe 渲染值时不转义
- capitalize 把值的首字母转换成大写，其他字母转换成小写
- lower 把值转换成小写形式 
- upper 把值转换成大写形式 
- title 把值中每个单词的首字母都转换成大写 
- trim 把值的首尾空格去掉 
- striptags 渲染之前把值中所有的 HTML 标签都删掉

模板中的控制结构

``` jinja2
<!-- 条件控制 -->
{% if user %}
	hello,{{ user }}!
{% else %}
	hello,stranger!
{% endif %}

<!-- 循环控制 -->
<ul>
	{% for comment in comments%}
		<li> {{comment}} </li>
	{% endfor %}
</ul>

<!-- 宏【类似函数】 -->
{% macro reder_comment(comment) %}
	<li> {{commont}} </li>
{% endmacro%}
<ul>
	{% for comment in comments %}
		{{ render_comment(comment) }}
	{% endfor %}
</ul>

<!-- 重复使用宏【放在文件中】 -->
{% import 'macros.html' as macros%}
<ul>
	{% for comment in comments %}
		{{ macros.render_comment(comment) }}
	{% endfor %}
</ul>

<!-- 多处使用的模板片段 -->
{% include 'comment.html'%}

<!-- 模板继承 -->
<!-- 基模板 -->
<html>
<head>
	{% block head %}
	<title>{% block title %}{% endblock %} - my</title>
	{% endblock %}
<\html>
<!-- 衍生模板【重定义】 -->
{% extends "base.html" %}
{% block title%} index {% endblock %}
{% block head %}
	{{ super() }} 
{% endblock %}
```

自定义错误页：

1. 使用errorhandler作为错误页的路由
2. 自定义404.html等页面
3. 用render_template渲染

模板中自动生成链接：url_for函数可以使用程序 URL 映射中保存 的信息生成 URL

## 静态文件

内容：图片、JavaScript 源码文件和 CSS

path：默认static子目录

## 重定向

设置原因：为刷新页面时浏览器会重新发送之前已经发送过的最后一个请求，为了最后一个请求不是post的情况，最好别让post作为最后一个请求

重定 向是一种特殊的响应，响应内容是 URL，而不是包含 HTML 代码的字符串。浏览器收到 这种响应时，会向重定向的 URL 发起 GET 请求，显示页面的内容。

数据传递：为了能在请求之间记住数据，因此可以使用会话来保存数据。

## 数据库

使用方法

1. 数据库引擎 ：mysql、mongdb
2. 数据库抽象层代码包ORM/ODM：SQLAlchemy

选择因素：

- 易用性：抽象层能直接使用面向对象的操作
- 性能：ORM与ODM会有损耗
- 可移植性：抽象层支持更多
- flask集成度：抽象层集成更多的数据库

SQLAlchemy使用方法：

```python
#定义一个SQLAlchemy对象
db = SQLAlchemy(app)

#表的增删，更新表结构的方法只能先删除再创建
db.creaye_all()
db.drop_all()

#创建模型，此时还没写入数据库
>>> from hello import Role, User
>>> admin_role = Role(name='Admin')
>>> mod_role = Role(name='Moderator')
>>> user_role = Role(name='User')
	#外键对应
>>> user_john = User(username='john', role=admin_role)
>>> user_susan = User(username='susan', role=user_role)
>>> user_david = User(username='david', role=user_role)

#通过数据库会话管理对数据库的行进行改动
>>> db.session.add(admin_role)
>>> db.session.add(mod_role)
>>> db.session.add(user_role)
>>> db.session.add(user_john)
>>> db.session.add(user_susan)
>>> db.session.add(user_david)
#或者
>>> db.session.add_all([admin_role, mod_role, user_role,
... user_john, user_susan, user_david])

#提交会话[事务]
>>> db.session.commit()
#事务回滚
db.session.rollback()

#行的改
>>> admin_role.name = 'Administrator'
>>> db.session.add(admin_role)
>>> db.session.commit()
#行的删
>>> db.session.delete(mod_role)
>>> db.session.commit()

#查询行-每个模型类都有query查询对象
#查询所有
>>> Role.query.all()
[<Role u'Administrator'>, <Role u'User'>]
>>> User.query.all()
[<User u'john'>, <User u'susan'>, <User u'david'>]
#过滤查询
>>> User.query.filter_by(role=user_role).all()
[<User u'susan'>, <User u'david'>]

#抽象还原为原生数据库语句[未添加触发查询的执行函数]
>>> str(User.query.filter_by(role=user_role))
'SELECT users.id AS users_id, users.username AS users_username,
users.role_id AS users_role_id FROM users WHERE :param_1 = users.role_id'

#从数据库中抽取一个模型
>>> user_role = Role.query.filter_by(name='User').first()
```

## 模型

定义：表示程序使用的持久化实体，一般是一个 Python 类，类中 的属性对应数据库表中的列，包括一些辅助函数

```python
db = SQLAlchemy(app)
#定义示例
class Role(db.Model):
 	__tablename__ = 'roles'
 	id = db.Column(db.Integer, primary_key=True)
 	name = db.Column(db.String(64), unique=True)
    #定义反向关系
    users = db.relationship('User', backref='role') 
 	def __repr__(self):
 		return '<Role %r>' % self.name 

class User(db.Model):
 	__tablename__ = 'users'
 	id = db.Column(db.Integer, primary_key=True)
 	username = db.Column(db.String(64), unique=True, 		index=True)
    #设置外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
 	def __repr__(self):
	 	return '<User %r>' % self.username
```



## 数据迁移

使用Flask-Migrate实现数据库迁移

步骤

1. 创建迁移仓库
2. 创建迁移脚本
3. 更新数据库

```python
#创建migrate类
migrate = Migrate(app, db)
#可附加到 FlaskScript 的 manager 对象上方便在shell中调用
#MigrateCommand 类使用 db 命令附加
manager.add_command('db', MigrateCommand)

#创建迁移仓库，会创建 migrations 文件夹，所有迁移脚本都存放其中
(venv) $ python hello.py db init 

#创建迁移脚本
#使用 revision 命令手动创建 Alembic 迁移，也可使用 migrate 命令自动创建。手动创建只会有空的upgrade() 和 downgrade() 函数，自动创建则帮你填好了
#upgrade() 函数把迁移中的改动应用到数据库中，downgrade() 函数则将改动删除。
(venv) $ python hello.py db migrate -m "initial migration"

#运行迁移脚本
#upgrade 命令能把改动应用到数据库中，且不影响其中保存的数据
(venv) $ python hello.py db upgrade 
```



## 集成python shell

用修饰符@app.shell_context_processor来修饰函数就可以达到启动shell会话时自动导入的目的

## 电子邮件

发送方式

1. smtplib包
2. Flask-Mail扩展

Flask-Mail 连接到简单邮件传输协议（Simple Mail Transfer Protocol，SMTP）服务器，并 把邮件交给这个服务器发送。如果不进行配置，Flask-Mail 会连接 localhost 上的端口 25， 无需验证即可发送电子邮件。其send函数使用了current_app，必须激活程序上下文

敏感信息：最好让脚本从环境中导入敏感信息

发送邮件的延迟解决方法：后台再开辟一个线程，或者把任务发给 [Celery](http://www.celeryproject.org/)任务队列

## 大型web程序的组织

```
#基本结构
|-flasky
 	|-app/        Flask 的所有程序一般都保存在名为 app 的程序包中
 		|-templates/  存放模板
 		|-static/     存放静态文件
 		|-main/   以结构化的方式定义蓝本模块包
 			|-__init__.py  创建蓝本
 			|-errors.py	错误处理程序
 			|-forms.py  表单对象
 			|-views.py	程序的路由/视图函数
 		|-__init__.py   定义程序的工厂函数，延迟程序实例的创建
 		|-email.py
 		|-models.py
 	|-migrations/    migrations 文件夹包含数据库迁移脚本
 	|-tests/         单元测试编写在 tests 包中
 		|-__init__.py
  		|-test*.py
 	|-venv/          venv 文件夹包含 Python 虚拟环境
 	|-requirements.txt 列出了所有依赖包
 	|-config.py      存储配置
 	|-manage.py		 用于启动程序以及其他的程序任务
```

配置文件：是开发、测试和生产环境要使用不同的数据库，因此需要不同的配置，设置一个init_app用以执行对当前 环境的配置初始化

app/init：init中定义一个工厂函数，延迟创建程序实例，把创建过程移到可显式调用的工厂函数中，给脚本留出配置程序的时间，还能够创建多个程序实例，便于测试。且需要注册蓝本

蓝本：蓝本和程序类似，也可以定义路由。不同的 是，在蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上后，路由才真正成为程序 的一部分。使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。

app/main/init：通过实例化一个 Blueprint 类对象可以创建蓝本。这个构造函数有两个必须指定的参数： 蓝本的名字和蓝本所在的包或模块。和程序一样，大多数情况下第二个参数使用 Python 的 _name _ 变量即可。循环导入时，导入放在末尾可以避免

app/main/errors：在蓝本中编写错误处理程序稍有不同，如果使用 errorhandler 修饰器，那么只有蓝本中的 错误才能触发处理程序。要想注册程序全局的错误处理程序，必须使用 app_errorhandler。

app/main/views：在蓝本中编写视图函数主要有两点不同：第一，和前面的错误处理程序一样，路由修饰器 由蓝本提供；第二，url_for() 函数的用法不同。Flask 会为蓝本中的全部端点加上一个命名空间，这样就可以在不 同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。命名空间就是蓝本的名字 （Blueprint 构造函数的第一个参数），所以视图函数 index() 注册的端点名是 main.index， 其 URL 使用 url_for('main.index') 获取。url_for() 函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如 url_for('. index')。在这种写法中，命名空间是当前请求所在的蓝本。

app/main/forms：表单对象也要移到蓝本中

tests：何使用 Python 的 [unittest](https://docs.python.org/2/library/unittest.html) 包编写测试

## 不会的点

- 测试单元的编写
- shell脚本相关