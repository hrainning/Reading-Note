#会查找所有模块并查找测试
import unittest
from flask import current_app
from app import create_app,db


class BasicsTestCase(unittest.TestCase):

    #测试前运行
    #构建一个测试环境
    def setUp(self):
        #创建程序
        self.app = create_app('testing')
        #上下文推送激活，确保能使用currentapp
        self.app_context = self.app.app_context()
        self.app_context.push()
        #建立数据库
        db.create_all()

    #测试后运行
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #test_开头的均作为测试运行
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertFalse(current_app.config['TESTING'])
