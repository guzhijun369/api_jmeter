# coding=utf-8
import requests
import json
import re
from jsonpath import jsonpath
from loguru import logger
from importlib import import_module
import types
from unittest import mock
from config.globalparam import json_path,custom_function_file


false = False  # 用于转义send_data中存在的false,true,null，python中没有这种关键字，转成对应的
true = True
null = None

class SendRequest(object):

    def __init__(self, url=None, headers=None, mock=mock):
        self.url = url
        self.headers = headers
        self.mock = mock
        self.global_func_dic = self.init_funcs(custom_function_file)  # 初始化加载自定义函数

    def send_file_data(self, url, dict=None, file_name=None):
        re = requests.post(url, data=dict, files=file_name)
        print('url:{}\r\nmethod:{}\r\nrequest_data:{}\r\nresponse:{}'.format(url, 'post', dict, re.json()))
        return re.json()

    def send_request(self, method, url, data=None, header=None, extract=''):
        """
        :param method: 请求方法
        :param url:  请求url
        :param data:  请求Body
        :param header:  请求头
        :param extract:  对返回结果进行变量提取
        :return: r.json()
        """
        re = None
        re_error = {'msg': '请求失败',
                    'code': '请求失败'}
        re_type_error = {
            'code': 10001,
            'msg': '返回数据格式不是json，当前框架无法处理，请联系框架开发者--谷哥'
        }
        if method == 'get':
            try:
                re = requests.get(url, headers=header)
            except Exception as e:
                return e
        elif method == 'post':
            if header['Content-Type'] == 'application/x-www-form-urlencoded':
                try:
                    re = requests.post(url, data=data, headers=header)
                except Exception as e:
                    return e
            elif header['Content-Type'] == 'text/xml':
                try:
                    re = requests.post(url, json=data, headers=header)
                except Exception as e:
                    return e
            elif header['Content-Type'] == 'application/json':
                try:
                    re = requests.post(url, json=data, headers=header)
                except Exception as e:
                    return e
            elif header['Content-Type'] == 'multipart/form-data':
                try:
                    del header['Content-Type']
                    re = requests.post(url, data=data, headers=header)
                except Exception as e:
                    return e
            else:
                re = False
        elif method == 'delete':
            try:
                re = requests.delete(url, headers=header)
            except Exception as e:
                return e
        elif method == 'patch':
            try:
                re = requests.patch(url, headers=header)
            except Exception as e:
                return e
        print('url:{}\r\nmethod:{}\r\nrequest_data:{}'.format(url, method, data))
        if re and re.status_code == 200:
            print('response_code: {}'.format(re.status_code))
            try:
                re_json = re.json()
                print('response:{}'.format(re_json))
                if extract != '':
                    self.operate_json(re_json, extract)
                return re_json
            except:
                print('response:{}'.format(re_type_error))
                return re_type_error
        else:
            print('response_code: {}'.format(re.status_code))
            print('url:{}\r\nmethod:{}\r\nrequest_data:{}\r\nresponse:{}'.format(url, method, data, '请求失败'))
            return re_error

    def send_request_all(self, data):
        """
        :param data: 从data文件中读取到的对应接口数据
        :return: r.json()
        """
        global false, true, null   # 兼容send_data中的true,false,null
        if 'http' in data['url']:  # url如果是比较少见的不属于本项目域名，可以直接配置完整域名
            url = data['url']
        else:
            url = self.url + data['url']
        method = data['method']
        send_data = data['send_data']
        extract = data['extract']
        rely = data['rely']
        content_type = data['Content-Type']
        if 'mock_data' in data:
            if send_data != '':
                send_data = eval(send_data)
            r =self.mock_test(method, url, send_data, self.headers, data['mock_data'])
            print('url:{}\r\nmethod:{}\r\nrequest_data:{}\r\nmock返回值 response:{}'.format(url, method, send_data, r))
            if extract != '':
                self.operate_json(r, extract)
            return r
        if content_type is None or content_type == '':
            content_type = 'application/json'
        self.headers['Content-Type'] = content_type
        if rely == 'no':
            if '{' in send_data and '}' in send_data:
                send_data = eval(send_data)
            r = self.send_request(method, url=url, data=send_data, header=self.headers)
        else:
            global_var_dic = self.operate_json()
            if method == 'post' or method == 'put':
                send_data = eval(self.replace_all_var(send_data, global_var_dic))
                r = self.send_request(method, url=url, data=send_data, header=self.headers, extract=extract)
            else:
                url = self.replace_all_var(url, global_var_dic)
                r = self.send_request(method, url=url, data=send_data, header=self.headers, extract=extract)
        # write_res(rownum, json.dumps(r, indent=2, ensure_ascii=False))  # 写入返回值
        return r

    def mock_test(self, method, url, send_data, header, mock_res_data):
        """
        封装Mock请求方法
        :param method: 同send_request
        :param url: 同send_request
        :param send_data: 同send_request
        :param header: 同send_request
        :param mock_res_data: 同send_request
        :return: 配置的mock返回值
        """
        mock_method = self.mock.Mock(return_value=mock_res_data)
        res = mock_method(method, url, send_data, header)
        return res

    def json_exact_search(self, data, key):
        '''
        # 精确提取：json.data.name
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
        logger.info('————json方法：精确查找提取-查找条件：%s,%s' % (type(key), key))
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
            logger.info('————json方法：精确查找-提取值：————%s,%s' % (type(v), v))
            return v
        except Exception as e:
            logger.debug('————json方法：精确查找-错误：————%s' % e)
            return None
        finally:
            logger.debug('————json方法：精确查找-结束————')

        # 精确提取：data[][][]

    def data_exact_search(self, datas, key):
        '''
        :param data: 嵌套字典、列表；dict、list；示例：{'code':0,'data':[{'name':'a'},{'name':'b'},{'name':'c'}]}
        :param key:  查找条件；str；示例："$.['data'][0][name]"    ,jsonpath提取规则
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
            res = jsonpath(data, key)
            logger.info('————data方法：精确查找提取-开始查找————%s,%s' % (type(res), str(res)))
        except:
            res = None
            logger.debug('data方法：精确查找提取-查找失败:%s,%s' % (type(res), res))
        return res

    def load_func_tools(self, module):
        """
        加载自定义函数
        :param module: 自定义函数引用路径
        :return: 函数对象
        """
        try:
            module_functions = {}
            module = import_module(module)
            if module:
                for name, item in vars(module).items():
                    if isinstance(item, types.FunctionType):
                        module_functions[name] = item
            return module_functions
        except Exception:
            return {}

    def replace_func(self, p, cache):
        """
        替换send_data中所有{}包含的变量
        :param p: send_data 字符串'{"id":{name}, "page": 1}'
        :param cache: 变量存储的字典，即json文件读取出来的数据
        :return: 替换后数据，str
        """
        func_matcher = re.compile(
            r"[\$]{1}[\{]{1}"  # 可以匹配${}的函数
            r"([0-9a-zA-Z_.=]+)"  # 匹配函数名称可以包含.
            r"[ ]*"  # 函数方法名称后0或多个空格
            r"\((.*?)\)"  # 匹配函数参数
        )
        if isinstance(p, str) and func_matcher.findall(p):
            for fn_tuple in func_matcher.findall(p):
                fun, varials = fn_tuple[0], fn_tuple[1]
                fnc_map = cache.get("FUNCS")
                try:
                    fn_raw = "{fun}({varials})".format(fun=fun, varials=varials)
                    fn = "{fun}({varials})".format(fun=fun, varials=varials)
                    target_data = eval(fn, fnc_map)
                    p = p.replace('${', '{').replace("{" + fn_raw + "}", str(target_data))
                except (ModuleNotFoundError, ImportError) as e:
                    logger.debug("函数没找到或者导入失败", p, cache)
                except NameError as e:
                    logger.debug("err", e)
        return p

    def operate_json(self,res_data=None, extract=None):
        """
        操作全局变量json文件，参数都传时为写入全局变量，参数都不传时为读取全局变量，同真同假
        :param res_data: 接口返回数据
        :param extract:  提取表达式字典，key为存储的全局变量名，value为返回值提取表达式{"id":"json.data.id"}
        :return:
        """
        if res_data and extract is None:
            logger.error('参数不符合规则')
            return
        if extract and res_data is None:
            logger.error('参数不符合规则')
            return
        with open(json_path, 'r', encoding='utf-8') as rf:
            load_dict = json.load(rf)
        if extract is None:
            return load_dict
        for k, v in extract.items():
            value = self.json_exact_search(res_data, v)
            if value:
                load_dict[k] = value
                logger.debug('返回值提取到全局变量{}:{}'.format(k, value))
        with open(json_path, 'w', encoding='utf-8') as wf:
            json.dump(load_dict, wf, indent=4, ensure_ascii=False)
            wf.write('\n')

    def init_funcs(self, model):
        """
        初始化自定义函数方法
        :param model: 自定义函数引用路径
        :return:
        """
        load_dict = {}
        load_dict['FUNCS'] = self.load_func_tools(model)
        return load_dict

    def replace_variable(self, p, cache):
        """
        替换send_data中所有{}包含的变量
        :param p: send_data 字符串'{"id":{name}, "page": 1}'
        :param cache: 变量存储的字典，即json文件读取出来的数据
        :return: 替换后数据，str
        """
        varial_matcher = re.compile(
            r"\{([\w.]+)\}"
            r"|\$\{([\w.]+)\}"  # 匹配$开头并{}包括的变量
        )
        if isinstance(p, str) and varial_matcher.findall(p):
            variables_list = []
            try:
                for var_tuple in varial_matcher.findall(p):
                    variables_list.append(
                        var_tuple[0] or var_tuple[1]
                    )
                for items in variables_list:
                    items_list = items.split('.')
                    target_data = cache
                    for i in items_list:
                        target_data = target_data.get(i, {})
                    if target_data != {}:
                        p = p.replace("{" + items + "}", str(target_data))
                return p

            except Exception as e:
                logger.error(e)
                logger.error(p)
        return p

    def replace_all_var(self, p, cache):
        """
        替换请求参数中带${}和{}的函数/变量
        :param p: sting 元素请求数据
        :param cache: 提取的全局变量字典，读取自json文件
        :return:
        """
        replace_var = self.replace_variable(p, cache)
        replace_func = self.replace_func(replace_var, self.global_func_dic)
        return replace_func
if __name__ == '__main__':
    s = SendRequest().load_func_tools('custom_function')
    print(s)



