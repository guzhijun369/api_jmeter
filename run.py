#coding=utf-8
import unittest
import HTMLTestRunner
import time
import os
from loguru import logger
from config import globalparam
from public.send_report import SslSendReport

path = os.path.join(globalparam.log_path,'test_{}.log'.format(time.strftime('%Y-%m-%d')))

logger.add(path, level=globalparam.log_level, enqueue=True)  # 日志初始化


def run(method, test=None):
    if method == 'all':
        start_time = int(time.time())
        test_dir = './testcase'
        suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test_*.py')
        now = time.strftime('%Y-%m-%d_%H_%M_%S')
        reportname = os.path.join(globalparam.report_path, 'TestResult' + now + '.html')
        with open(reportname, 'wb') as f:
            runner = HTMLTestRunner.HTMLTestRunner(
                stream=f,
                verbosity=2,
                title='测试报告',
                description='输出如下报告'
            )
            runner.run(suite)
        #  判断环境变量，线上就发钉钉报告
        if os.environ.get('RUN_MODE') == 'testpro':
            send_report = SslSendReport()
            send_report.main_pro(start_time)
        # 发送邮件
        #mail = sendmail.SendMail()
        #mail.send()
    if method == 'one':
        suit = unittest.TestSuite()
        suit.addTest(test)  # 把这个类中需要执行的测试用例加进去，有多条再加即可
        runner = unittest.TextTestRunner()
        runner.run(suit)

if __name__ == '__main__':
    # run('one', test_3_project.Project("test_6_enable_project"))
    run('all')