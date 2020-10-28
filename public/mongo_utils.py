#coding=utf-8
import pymongo
from urllib import parse
from config.basic_config import ConfigInit
from faker import Faker
import random
from loguru import logger


fake = Faker("zh_CN")
fake_en = Faker("en_US")

def connect_sql():
    """连接mongodb"""
    user = parse.quote_plus(ConfigInit.mongo_user)
    pw = parse.quote_plus(ConfigInit.mongo_pw)
    client = pymongo.MongoClient('mongodb://{}:{}@{}/'.format(user, pw, ConfigInit.mongo_ip_port))

    return client

def updata_project(db, name):
    mongo_db = db['jimi-platform']
    t_project = mongo_db['t_project']
    condition = {
    "name": "接口测试",
    "remark": "wwww",
    }
    # 找到信息
    student = t_project.find_one(condition)
    # 更新后的信息
    student['name'] = name
    student['remark'] = "aaaaa"
    result = t_project.update_one(condition, {'$set': student})
    logger.info('project 表数据修改成功')


def updata_info(db, name, company, phone):
    mongo_db = db['jimi-platform']
    t_organization_info = mongo_db['t_organization_info']
    condition = {
    "name": "接口测试公司",
    "company": "接口测试公司",
    "linkman": "谷哥",
    "contact": "130288123881",
    }
    # 找到信息
    student = t_organization_info.find_one(condition)
    # 更新后的信息
    student['name'] = name
    student['company'] = company
    student['contact'] = str(phone)
    result = t_organization_info.update_one(condition, {'$set': student})
    logger.info('t_organization_info 表数据修改成功')

def updata_account(db, email, company):
    mongo_db = db['jimi-platform']
    t_organization_account = mongo_db['t_organization_account']
    condition = {
    "username": "2818783121@qq.com",
    "nickname": "接口测试公司",
    }
    # 找到信息
    student = t_organization_account.find_one(condition)
    # 更新后的信息
    student['username'] = email
    student['nickname'] = company
    result = t_organization_account.update_one(condition, {'$set': student})
    logger.info('t_organization_account 表数据修改成功')

def update_project_info():
    """修改项目信息"""
    email = fake.email()
    phone = fake.phone_number()
    company = fake.company()
    project_name =  "脚本修改" + fake.word() + str(random.randint(1,1000)) + "项目"
    db = connect_sql()
    updata_project(db, project_name)
    updata_info(db, project_name, company, phone)
    updata_account(db, email, company)

def update_product():
    db = connect_sql()
    code = fake_en.word()
    mongo_db = db['jimi-platform']
    t_product = mongo_db['t_product']
    condition = {
    "code": "TEXT"
    }
    # 找到信息
    student = t_product.find_one(condition)
    # 更新后的信息
    student['code'] = code
    result = t_product.update_one(condition, {'$set': student})
    logger.info('t_product 表数据修改成功')



if __name__ == '__main__':
    # update_project_info()
    db = connect_sql()
