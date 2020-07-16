# 博客

## 用户认证

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
- LoginManager类：设置登录信息保护等级、登录端点、自定义加载用户的回调函数
- itsdangerous类：生成令牌并检验，可用以发送确定用户的邮箱是否为真实的确认链接

功能点：

- 密码加密与检验
- 登录/登出/注册/找回密码
- 发送邮箱
- 用户信息管理
- 用户信息保存

## 用户角色

功能点：

- 权限/角色存储形式
- 赋予角色
- 角色检验

## 用户资料

功能点:

- 用户个人信息
- 用户信息展示
- 用户信息编辑
- 用户头像

## 博客文章

功能点：

- 提交和编写
- 资料页中展示
- 分页显示所有博客
- 博客编辑器和markdown格式

## 关注者

功能点

- 关注者存储形式与查询
- 显示关注者

## 用户评论

功能点：

- 评论的存储
- 评论的提交和显示
- 评论的管理

# API编写

