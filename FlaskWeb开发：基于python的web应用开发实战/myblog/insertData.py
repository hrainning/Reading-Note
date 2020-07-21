from app.models import Role,User,Post
from app import db,create_app

# 创建程序
app = create_app('default')
# 推送上下文
app_ctx = app.app_context()
app_ctx.push()

#删除旧表，建立新表
db.drop_all()
db.create_all()

#插入数据
Role.insert_roles()
user_admin = User(username='Administreator',account=123,password='123')

'''
user_john = User(username='john',account=1234, password='123')
user_susan = User(username='susan',account=2345, password='123')
user_david = User(username='david',account=3456, password='123')




#加入数据库管理会话

db.session.add(user_john)
db.session.add(user_susan)
db.session.add(user_david)

db.session.commit()
'''
User.generate_fake(100)
Post.generate_fake(100)

app_ctx.pop()