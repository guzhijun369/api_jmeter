#coding=utf-8
import werkzeug.security as wer
from faker import Faker
import random

fake = Faker("zh_CN")
fake_en = Faker("en_US")



def price_calculation(price):
    return price + '22223'

def passwd_hash(pw):
    return wer.generate_password_hash(pw)

def label():
    # 生成随机课程名称
    return fake.word()
def get_name():
    # 生成随机Name  # 生成随机课程标签
    name = "脚本修改" + fake.word() + str(random.randint(1, 1000)) + "课程"
    return name
def objector():
    # 生成随机目标学员
    return fake.word()
def income():
    # 生成随机学习目标
    return fake.sentence(nb_words=6, variable_nb_words=True)
def intro():
    # 生成随机课程综述
    return fake.sentence(nb_words=6, variable_nb_words=True)



