这是一个接口自动化框架，内容构成：python+unittest+request+ddt，编写人：谷志军

目录结构说明：

config/  配置文件目录

    basic_config  私人配置参数，url，邮箱账号密码等
    
    globalparam   项目配置文件，配置日志路径、截图路径、报告路径、浏览器、静默模式、数据读取路径等
    
data/  数据驱动文件存放路径
    global_variable_dict.json 全局变量存储文件

public/  各种方法封装


    custom_function.py  自定义函数
    
    data_info  读取数据文件方法
        
    mongo_utils   连接mongodb
        
    mysql_utils   连接mysql
        
    redis_utils   连接redis
        
    mytest        unittest基类，封装一些每个用例前后都要进行的操作,可以写多个基类，区分场景继承
        
    send_request    发送请求方法封装
        
    sendmail      发送测试报告方法，由于国内邮件服务经常被封，采用了国外的mailgun  smtp
    
report  测试生成数据目录

    html_report  测试报告存放路径
    
    logs  log日志存放路径
    
testcase  用例写在这个目录

run  框架入口，包含log初始化、生成测试报告、配置运行指定单个或者全部用例

