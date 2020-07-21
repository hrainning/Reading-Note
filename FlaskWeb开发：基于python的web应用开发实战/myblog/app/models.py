from datetime import datetime

import bleach
from markdown import markdown

from . import db
#密码散列以及检验
from werkzeug.security import generate_password_hash, check_password_hash

#自带实现
#is_authenticated：已经登录状态
#is_active：账号允许登录，活跃的账号
#is_anonymous：是否匿名
#git_id：用户的唯一标识
from flask_login import UserMixin,AnonymousUserMixin,login_manager

#权限常量
class Permission:
    FOLLOW = 0X01
    COMMENT = 0X02
    WRITER_ARITICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0X80

#定义模型
class Role(db.Model):
    #表名
    __tablename__='roles'
    #表的变量
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    #定义一个反向引用关系role，可以代替id来访问模型
    users = db.relationship('User',backref='role',lazy='dynamic')
    #返回表示模型的可读字符串
    def __repr__(self):
        return '<Role %r>' % self.name

    #将角色添加到数据库中
    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITER_ARITICLES,True),
            'Moderator':(Permission.FOLLOW|
                         Permission.COMMENT|
                         Permission.WRITER_ARITICLES|
                         Permission.MODERATE_COMMENTS,False),
            'Administreator':(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Follow(db.Model):
    __tablename__='follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)


class User(UserMixin,db.Model):

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.username == 'Administreator':
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()

        self.follow(self)
    __tablename__='users'


    id = db.Column(db.Integer,primary_key=True)
    account = db.Column(db.String(64),unique=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(64))
    #不加入邮箱功能，默认是已经验证过的人
    confirmed = db.Column(db.Boolean, default=True)
    #定义外键
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower',lazy='joined'),
                               lazy='dynamic',
                               cascade='all,delete-orphan')
    followers = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed',lazy='joined'),
                               lazy='dynamic',
                               cascade='all,delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    #读取时会raise错误
    #设置函数名为属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #设置时自动调用
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def can(self,permissions):
        return self.role is not None and\
               (self.role.permissions & int(permissions)) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    #刷新用户的最新请求时间，放在hoop中正好合适
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    #自动生成虚拟用户
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed,shuffle
        import forgery_py
        import string

        seed()
        for i in range(count):
            try:
                digit = list(string.digits)
                shuffle(digit)
                u = User(account=''.join(digit),
                         username=forgery_py.internet.user_name(True),
                         password=forgery_py.lorem_ipsum.word(),
                         confirmed=True,
                         location=forgery_py.address.city(),
                         about_me=forgery_py.lorem_ipsum.sentence(),
                         member_since=forgery_py.date.date(True)
                         )

                db.session.add(u)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    @property
    def followed_posts(self):
        return Post.query.join(Follow,Follow.followed_id==Post.author_id)\
                    .filter(Follow.follower_id == self.id)

    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None
    def __repr__(self):
        return '<User %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False


#无法实现重载，待解决
login_manager.anonymous_user = AnonymousUser

class Post(db.Model):

    __tablename__='post'

    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0,user_count -1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        #先转换到html
        #clean删除不允许的标签
        #linkify将url转换为适当的<a>
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_formate='html'),
            tags=allowed_tags,strip=True
        ))
#设置监听，自动调用
db.event.listen(Post.body,'set',Post.on_changed_body)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)


    #用以实现回调，能返回一个用户
from . import login_manager

# flask-login要求实现
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
