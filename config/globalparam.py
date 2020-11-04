#coding=utf-8
import os
import time
from loguru import logger


#项目路径
project_path = os.path.abspath('.')
if 'testcase' in project_path:
    project_path = os.path.join(project_path, "..")
if 'public' in project_path:
    project_path = os.path.join(project_path, "..")
# 日志路径
log_path = os.path.join(project_path,'report', 'logs')
if not os.path.exists(log_path):  # 如果路径不存在，创建路径
    os.makedirs(log_path)
# 测试报告路径
report_path = os.path.join(project_path, 'report', 'html_report')
if not os.path.exists(report_path):  # 如果路径不存在，创建路径
    os.makedirs(report_path)

log_level = 'INFO'

# 测试数据路径
data_path = os.path.join(project_path, 'data', 'testdata')

# json文件路径
json_path = os.path.join(project_path, 'data', 'global_variable_dict.json')
if not os.path.exists(json_path):  # 如果路径不存在，创建路径
    os.makedirs(json_path)
#自定义函数文件
custom_function_file = "public.custom_function"
if not os.path.exists(custom_function_file):  # 如果路径不存在，创建路径
    os.makedirs(custom_function_file)