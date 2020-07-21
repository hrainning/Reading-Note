# 博客

## 用户认证

功能点：

- 密码加密与检验
- 登录/登出/注册/找回密码
- 发送邮箱 * 
- 用户信息管理[修改密码/账号名]
- 用户信息保存

实现步骤：

1. 实现加密与检验密码的功能并测试
2. 创建专门用于用户认证的蓝本auth + view 
3. 注册蓝本
4. 构造准备用于登录的用户模型，使用flask-login扩展，实现登录状态、app的当前用户信息查询，限制授权的url等功能
5. flask-login要求实现一个能用指定标识服返回用户的回调
6. 构建登录表单
7. 设计template
8. 编写完整的view，使用login_user可以设置是否记住用户，若记住则cookie会长期保存，可用来复现用户会话
9. 构建注册表单
10. 设计template以及view
11. 构建修改密码、忘记密码、修改账号名的表单
12. 设计template以及view并整合到栏目中

python认证包：

- Flask-Login：管理已登录用户的用户会话。 
- Werkzeug：计算密码散列值并进行核对。
- itsdangerous：生成并核对加密安全令牌。

常规用途拓展包：

- Flask-Mail：发送与认证相关的电子邮件。
- Flask-Bootstrap：HTML 模板。 
- Flask-WTF：Web 表单。

密码加密[Werkzeug]：

- generate_password_hash(password, method= pbkdf2:sha1 , salt_length=8) :这个函数将原始密码作为输入,以字符串形式输出密码的散列值
- check_password_hash(hash, password) :这个函数的参数是从数据库中取回的密码散列值和用户输入的密码。返回值为 True 表明密码正确。

用于登录的用户模型[Flask-Login]：

- UserMixin类：实现对检查用户是否登录、禁用、普通以及返回用户id
- LoginManager类：设置登录信息保护等级、登录view、自定义加载用户的回调函数
- itsdangerous类：生成令牌并检验，可用以发送确定用户的邮箱是否为真实的确认链接

## 用户角色

功能点：

- 权限/角色存储形式
- 赋予角色
- 角色检验

步骤：

1. 创建权限常量
2. 构造角色模型及其方法
3. 定义用户默认角色，以及检查角色的功能
4. 定义检查角色权限的装饰器

## 用户资料

功能点:

- 用户个人信息
- 用户信息展示
- 用户信息编辑器
- 用户头像

步骤：

1. 更新用户模型
2. 添加显示界面与view
3. 创建用户信息编辑表单
4. 添加显示界面以及view
5. 创建管理员级别的表单
6. 创建管理员级别的view，并在profile界面中加按钮

## 博客文章

功能点：

- 提交和编写
- 资料页中展示
- 分页显示所有博客
- 博客编辑器和markdown格式转换
- 自动生成假用户与博客来使用[forgeryPy]

步骤：

1. 建立博客的model
2. 创建输入博客的form
3. 建立显示博客的view + template
4. 生成fake的博客和用户[forgeryPy]
5. 设置分页显示博客,Flask-SQLAlchemy 提供的 paginate() 方法
6. 创建分页的模板宏
7. 使用markdown和flask-pagedown支持富文本文章，添加拓展，使用富文本格式以及添加修改template
8. 将post到服务器的markdown文本转换为html，并存入post模型中 
9. 创建博客的view以及template单独显示
10. 建立修改博客的view + template

包与拓展：

- forgeryPy：生成模拟数据

- PageDown：使用 JavaScript 实现的客户端 Markdown 到 HTML 的转换程序。
- Flask-PageDown：为 Flask 包装的 PageDown，把 PageDown 集成到 Flask-WTF 表单中。
- Markdown：使用 Python 实现的服务器端 Markdown 到 HTML 的转换程序。 
- Bleach：使用 Python 实现的 HTML 清理器。

## 关注者

功能点

- 关注者存储形式与查询
- 显示关注者
- 首页显示关注者的博客

步骤：

1. 建立follow关系模型，并增加user模型的相关方法
2. 资料页中显示关注者
3. 编写关注、取关的view以及关注列表的template以及view和进入按钮
4. 加入查询关注者的博客的函数
5. 设置显示所有的view并修改template

## 用户评论

功能点：

- 评论的存储
- 评论的提交和显示
- 评论的管理

步骤：

1. 创建comment的模型，并建立一对多关系
2. 添加输入表单，以及view与template显示
3. 添加管理评论的按钮以及view
4. 创建管理评论的template

# API编写

# 测试用例编写

工具：unittest

类型：单元测试

基础测试：

- 正常启动，当前用例[current_app]存在
- 能够调整配置

用户认证功能测试：

- 加密成功
- 检验成功
- 不许访问
- 散列随机

获取代码覆盖报告工具：recover

测试客户端[利用url发送请求，利用返回值判断是否成功]：

- 进入首页
- 注册并登录账号
- 若有api则可以编写代码测试

Selenium测试：向web浏览器发送指令，不直接与程序交互，测试各个功能

# 性能优化

数据库查询：

- 通过数据库提供的explain查看数据库查询采取的步骤
- 设置阈值，把超时的都记录到日志中

代码效率：

- 大量运算的函数可导致cpu消耗，使用源码分析器能找出程序中执行最慢的部分
- Flask 使用的开发 Web 服务器由 Werkzeug 提供，可根据需要为每条请求启用 Python 分析 器。

# 部署

步骤：

1. 安装数据库等必要环境
2. 安装适用于生产环境的 Web 服务器，例如 Gunicorn 或 uWSGI。
3. 编写部署的代码，如创建数据库等
4. 令程序运行在服务器中
5. 可选：反向代理nginx、ssl证书、防火墙等

