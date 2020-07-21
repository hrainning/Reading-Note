import os

#项目地址
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'sajdkhaskdkjas'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE = 10
    FOLLOWERS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,'data.sqlite')

class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.environ.get('TEST_DATABASE_URL') or \
                               'sqlite:///' + os.path.join(basedir,'test.sqlite')

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or \
                               'sqlite:///' + os.path.join(basedir,'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}