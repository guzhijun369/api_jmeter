# coding=utf-8
import xlrd
import os
from config import globalparam
from xlutils.copy import copy
from loguru import logger
from jsonpath import jsonpath
from pprint import pprint

PATH = globalparam.data_path

# print(PATH)
def get_excel_dict(path, index=0):
    paralList=[]
    paraldict={}
    dirs = os.listdir(path)
    for filename in dirs:
        workbook=xlrd.open_workbook(os.path.join(globalparam.data_path,filename))  # 打开文件
        sheet=workbook.sheets()[index]  # sheet索引从0开始
        firstRowDataList=sheet.row_values(0)#第一行数据
        # file_dict = []
        for rownum in range(1, sheet.nrows):#循环每一行数据
            list = sheet.row_values(rownum)
            dict={}
            dictTestCaseName={}
            for i in range(len(list)):
                dict['rownum'] = rownum  # 存储当前行数，以便返回数据写入
                dict[firstRowDataList[i]] = list[i]  # 每一行数据与第一行数据对应转为字典
                # json.dumps(json.loads(caseData), ensure_ascii=False)
            dictTestCaseName[list[0]] = dict  # 转为字典后与用例名字对应转为字典
            paralList.append(dictTestCaseName)
        paraldict[filename.split('.')[0]] = paralList  # 将处理后的数据放入列表里
    return paraldict

false = False  # 用于转义send_data中存在的false,true,null，python中没有这种关键字，转成对应的
true = True
null = None

def get_test_case_data(data_info, model, testCaseName):
    """
    :param data_info: 表数据
    :param model: 表名
    :param testCaseName: 用例名
    :return: 匹配数据
    """
    global false, true, null
    testData = data_info[model]
    getTestCaseDataList = []
    for data in testData:
        if (list(data.keys())[0]) == testCaseName:
            getTestCaseDatadict = {}
            if 'send_data' in data[testCaseName]:
                if '{' in data[testCaseName]['send_data'] and '}' in data[testCaseName]['send_data']:
                    getTestCaseDatadict['send_data'] = data[testCaseName]['send_data']  # 获取表中的send_data，即接口发送数据
                else:
                    getTestCaseDatadict['send_data'] = data[testCaseName]['send_data']
            else:
                getTestCaseDatadict['send_data'] = None
            getTestCaseDatadict['assert_info'] = eval(data[testCaseName]['assert_info'])  # 获取表中的assert_info，即断言数据
            getTestCaseDatadict['method'] = data[testCaseName]['method']  # 获取表中method，即请求方式
            getTestCaseDatadict['url'] = data[testCaseName]['url'].replace('\n', '').replace('\r',
                                                                                             '').strip()  # 获取表中url
            getTestCaseDatadict['case_name'] = data[testCaseName]['case_name'].replace('\n', '').replace('\r',
                                                                                                         '').strip()  # 获取表中case_name，即用例名称
            getTestCaseDatadict['rownum'] = data[testCaseName]['rownum']  # 获取当前数据行数，以便写入返回值
            getTestCaseDatadict['rely'] = data[testCaseName]['rely'].replace('\n', '').replace('\r', '').strip()  # 获取表中rely，yes/no，是否对请求参数检查变量替换
            if data[testCaseName]['extract'] != '':  # 返回值后置处理表达式
                getTestCaseDatadict['extract'] = eval(data[testCaseName]['extract'])
            else:
                getTestCaseDatadict['extract'] = ''
            if 'Content-Type' in data[testCaseName]:
                getTestCaseDatadict['Content-Type'] = data[testCaseName]['Content-Type'].replace('\n', '').replace('\r',
                                                                                                                   '').strip()
            else:
                getTestCaseDatadict['Content-Type'] = None
            if data[testCaseName]['has_mock'].replace('\n', '').replace('\r', '').strip() == 'yes':
                getTestCaseDatadict['mock_data'] = eval(data[testCaseName]['mock_data'])
            getTestCaseDataList.append(getTestCaseDatadict)
    return getTestCaseDataList


def write_res(rownum, data):
    # 将接口返回值写入文件，res_data
    oldwb = xlrd.open_workbook(PATH, formatting_info=True)
    newwb = copy(oldwb)
    sheet = newwb.get_sheet(0)
    sheet.write(rownum, 11, data)
    newwb.save(PATH)

def json_exact_search(data, key):
    '''
    :param data: 嵌套字典、列表；dict、list；示例：{'code':0,'data':[{'name':'a'},{'name':'b'},{'name':'c'}]}
    :param key:  查找条件; str ； 示例：'json.data.0.name'
    :return: 结果 = a
    '''
    logger.info('————精确提取：json方式————')
    if type(data) != dict:
        try:
            data = eval(data)
        except:
            return None
    logger.debug('————json方法：精确查找提取-数据源：%s,%s' % (type(data), data))
    logger.debug('————json方法：精确查找提取-查找条件：%s,%s' % (type(key), key))
    k_list = key.split('.')
    k_list.pop(0)
    try:
        for i in k_list:
            try:
                i = int(i)
            except:
                i = i
            logger.debug('————json方法：精确查找提取-提取条件：%s,%s' % (type(i), i))
            logger.debug('————json方法：精确查找提取-提取后数据源：%s,%s' % (type(key), key))
            v = data[i]
            data = v
        logger.debug('————json方法：精确查找-提取值：————%s,%s' % (type(v), v))
        return v
    except Exception as e:
        logger.debug('————json方法：精确查找-错误：————%s' % e)
        return None
    finally:
        logger.debug('————json方法：精确查找-结束————')

        # 精确提取：data[][][]


def data_exact_search(datas, key):
    '''
    :param data: 嵌套字典、列表；dict、list；示例：{'code':0,'data':[{'name':'a'},{'name':'b'},{'name':'c'}]}
    :param key:  查找条件；str；示例："$.['data'][0]['name']"    ,jsonpath提取规则
    :return: 结果 = a
    '''
    logger.info('————进入精确提取：data方式————')
    if type(datas) != dict:
        try:
            datas = eval(datas)
        except:
            return None
    data = datas
    logger.debug('data方法：精确查找提取-数据源：%s,%s' % (type(data), data))
    logger.info('data方法：精确查找提取-查找条件：%s,%s' % (type(key), key))
    try:
        res = jsonpath(data, key)[0]
        logger.info('————data方法：精确查找提取-开始查找————%s,%s' % (type(res), str(res)))
    except:
        res = None
        logger.debug('data方法：精确查找提取-查找失败:%s,%s' % (type(res), res))
    return res



if  os.path.exists(PATH):  # 如果路径不存在，创建路径
    data_info = get_excel_dict(PATH)
else:
    data_info = None
# pprint(data_info)
# a = get_test_case_data(data_info, 'data','login')
# #
# pprint(a)
