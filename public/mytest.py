# coding=utf-8
import unittest
from loguru import logger
from public.send_request import SendRequest
from config.basic_config import ConfigInit

class MyTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """
    def setUp(self):
        self.url = ConfigInit.url
        self.headers = {}
        self.send_requests = SendRequest(self.url, self.headers)
        logger.info('############################### START ###############################')

    def tearDown(self):
        logger.info('###############################  End  ###############################')


class MyTokenTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """

    @classmethod
    def login_func(cls, account='18175516432', pw='hb123456'):
        """封装登录函数"""
        send_data = {
            "account":account,
            "password":pw,
            "login_type":1 }
        url = ConfigInit.url + '/id_v2_5/user/login'
        headers = {'Content-Type': 'application/json'}
        r = SendRequest(url, headers).send_request("post", url=url, data=send_data, header=headers)
        token = r['data']['token']
        user_id = r['data']['basic']['id']
        return token,user_id

    @classmethod
    def setUpClass(cls):
        cls.token, cls.user_id = cls.login_func()

    def setUp(self):
        self.url = ConfigInit.url
        self.headers = {
                        'JK-TOKEN':self.token,
                        'JK-USER-ID': str(self.user_id)
                        }
        self.send_requests = SendRequest(self.url, self.headers)
        logger.info('############################### START ###############################')

    def tearDown(self):
        logger.info('###############################  End  ###############################')

    @classmethod
    def tearDownClass(cls):
        pass