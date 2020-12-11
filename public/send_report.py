#coding=utf-8
import os
from config import globalparam
from requests import request
import time
import shutil
from loguru import logger

reportPath = globalparam.report_path


class SslSendReport:

    def __init__(self):
        # self.ssh = paramiko.SSHClient()
        #
        # # 允许连接不在~/.ssh/known_hosts文件中的主机
        # self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # # private_key = paramiko.RSAKey.from_private_key_file(globalparam.ssh_hostkey)
        # # 连接服务器
        # self.ssh.connect(hostname="xxxxx", port=22, username="root", password="xxxxxx")
        pass

    def get_report(self):
        """获取最新测试报告"""
        dirs = os.listdir(reportPath)
        dirs.sort()
        dirs_html = []
        for filename in dirs:  # 找到文件夹中后缀为.html的最新的那个文件
            file, suffix = os.path.splitext(filename)
            if suffix == '.html':
                dirs_html.append(filename)
        newreportname = dirs_html[-1]
        print('The new report name: {0}'.format(newreportname))
        return newreportname

    def rm_oldreport(self):
        """删除index目录下的旧报告"""
        try:
            os.remove(r'/root/test/web/index.html')
            # os.remove(r'C:\Users\xxxx\Desktop\index.html')
            logger.info('删除旧报告成功')
        except Exception as e:
            logger.info('删除失败')

    def cp_report(self):
        """将最新报告移动到index目录下"""
        newreport = self.get_report()
        report_name = os.path.join(reportPath, newreport)
        logger.info(report_name)
        new_name = r'/root/test/web/index.html'
        # new_name = r'C:\Users\xxxx\Desktop\index.html'
        try:
            shutil.copyfile(report_name, new_name)
            logger.info('最新报告移动成功')
        except Exception as e:
            logger.info('移动报告失败:{}'.format(e))

    def send_dingding(self, start_time):
        """发送通知到钉钉"""
        now_time = int(time.time())
        time_consuming = now_time - start_time
        json = {
            "msgtype": "text",
            "text": {
                "content": "通知：PAAS4.0接口自动化运行完成，共耗时{} 秒，报告路径 http://172.16.0.124:9999/".format(time_consuming)
            }
        }
        url = 'xxxxxx'
        try:
            r = request('post', url, json=json)
            logger.info('发送警报成功')
        except Exception as e:
            logger.info('发送警报失败')

    def main_pro(self, start_time):
        self.rm_oldreport()
        self.cp_report()
        self.send_dingding(start_time)