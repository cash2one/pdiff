# coding=utf-8
'''
Created on 2013年10月28日

@author: liwei06
'''
import httplib
from urlparse import urlparse
import config
import json_diff
import optparse
import json
from json import JSONEncoder
import traceback




"""
比较两个Json字符串
ignore_value_keys: 数组，比较json时，不比较数组中key对应的Value，关于这个key的修改不放到比较结果中
ignore_key_keys:数组，比较json时，忽略数组中的key，关于这个key的删、改都不放到比较结果中。
"""
def compareResult(online, offline, ignore_value_keys, ignore_value_keys_fuzzy, ignore_key_keys,
    quick_mode=True, ignore_all_value_mode=False):
    options = optparse.Values()
    options.quick_mode = quick_mode
    options.exclude = ignore_key_keys
    options.include = []
    options.update_ignore = ignore_value_keys
    options.update_ignore_fuzzy = ignore_value_keys_fuzzy
    options.ignore_array_order = True
    options.ignore_append = True
    options.ignore_all_value_mode = ignore_all_value_mode
    diff = json_diff.Comparator(opts=options)
    diff_res = diff.compare_dicts(json.loads(online), json.loads(offline))
    return diff_res

def getRealTestUrl(testcase, executor):
        #合并case中指定的URL、参数
    if '?' in testcase.url:
        url = testcase.url + '&' + testcase.parameters
    else:
        url = testcase.url + '?' + testcase.parameters

    #确保url以&结束
    if (not url.endswith('&')) and (not url.endswith('?')):
        url = url + '&'
    #添加框架的默认参数
    for param in config.PDIFF_CONFIG['default_parameters']:
        url = url + param + '&'

    #设置执行机配置的Parameters

    for parameter in executor.defaultParameters:
        url = url + parameter[0] + '=' + parameter[1] + '&'

    return url

def request(hosturl, httpMethod, path, params, headers, report, server_description=''):

    requestResult = True

    #设置连接的Host
    conn = httplib.HTTPConnection(hosturl,timeout=10)
    tracecode = ""
    response_status = ""
    server_description = 'server ' + server_description + ' is not available'
    #请求URL
    try:
        conn.request(httpMethod, path, params, headers)
        response = conn.getresponse()
        tracecode = response.getheader('tracecode')
        response_status = str(response.status)
        if response.status != 200 :
            onlinedata = '{"tracecode":"%s","error":"%s","status_code":"%s"}' % (tracecode,server_description,response_status)
            requestResult = False
        else:
            onlinedata = response.read()
            datatmp = json.loads(onlinedata)
            datatmp['tracecode'] = tracecode
            onlinedata = JSONEncoder().encode(datatmp)
    except Exception,e:
        traceback.print_exc()
        onlinedata = '{"tracecode":"%s","error":"%s","status_code":"%s","errmsg":"%s"}' % (tracecode,server_description,response_status,str(e))
        requestResult = False
    #输出结果到文件
    f = open( report, 'w+')
    f.write(onlinedata)
    conn.close()

    return requestResult, onlinedata

def runTest(executor, testcase, testtarget, testcookie, testtargetsrc='ONLINE', report_folder=config.PDIFF_CONFIG['report_folder']):

    #设置执行机配置的UA、Refer、Cookies
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    headers['Referer'] = executor.referer
    headers['User-Agent'] = executor.ua
    headers['Cookie'] = ''
    for cookie in executor.cookies:
        headers['Cookie'] += cookie[0].upper() + '=' + cookie[1] + ';'
    #获取需要run的URL
    url = getRealTestUrl(testcase, executor)
    print 'realUrl:'+url

    #读取http method
    httpMethod = testcase.get_method().upper()
    if (not httpMethod == 'GET') and (not httpMethod == 'POST') :
        httpMethod = executor.get_method().upper()

    #解析参数
    o = urlparse(url);

    #指定输出文件路径
    if (not report_folder[-1] == '/') and (not report_folder[-1] == '\\'):
        report_folder = report_folder + '/'
    report_name = report_folder + testcase.get_name() + '@' + executor.get_name()
    if testtargetsrc == 'ONLINE':
        testtargetsrc=o.netloc
    else:
        testurl = config.URL_REPLACE[o.netloc]
        testtargetsrc = testurl.replace('HOST', testtargetsrc)
    print 'soureUrl:'+testtargetsrc
    #请求线上环境
    (online_status, onlinedata) = request(testtargetsrc, httpMethod, o.path + '?' + o.query, o.params, headers, report_name +  '.online.json', 'ONLINE')

    #retry once
    if not online_status :
        (online_status, onlinedata) = request(testtargetsrc, httpMethod, o.path + '?' + o.query, o.params, headers, report_name +  '.online.json', 'ONLINE')

    #请求测试环境
    #设置连接的Host, 如果testtarget未指定port，从配置中替换url
    if testtarget == 'ONLINE':
        testtarget=o.netloc
    else:
        testurl = config.URL_REPLACE[o.netloc]
        testtarget = testurl.replace('HOST', testtarget)
    print 'targetUrl:'+ testtarget
    #添加测试环境自定义cookie
    headers['Cookie'] = headers['Cookie'] + testcookie + ';'
    #请求测试URL
    (test_status, offlinedata) = request(testtarget, httpMethod, o.path + '?' + o.query, o.params, headers, report_name +  '.offline.json', 'TEST')
    #retry once
    if not test_status :
        (test_status, offlinedata) = request(testtarget, httpMethod, o.path + '?' + o.query, o.params, headers, report_name +  '.offline.json', 'TEST')

    #读取ignore配置
    ignore_value_keys = []
    ignore_value_keys_fuzzy = []
    ignore_all_value_mode = False


    for key in testcase.get_ignore_keys():
            ignore_value_keys.append(key)

    #need to ignore all value, only compare key structure
    if len(testcase.get_ignore_keys()) == 1 and testcase.get_ignore_keys()[0] == 'ALL_VALUE':
        ignore_all_value_mode = True
    else:
        for key in config.PDIFF_CONFIG['default_ignore_value_param']:
            ignore_value_keys.append(key)

    ignore_key_keys = config.PDIFF_CONFIG['default_ignore_key_param']
    #added by jiaolianxin
    ignore_value_keys_fuzzy = config.PDIFF_CONFIG['default_ignore_value_param_fuzzy']
    #end
    #将ignore配置写到文件中
    f = open(report_name + '.ignore_key_keys', 'w+')
    f.write(', '.join(ignore_key_keys))
    f = open(report_name + '.ignore_value_keys', 'w+')
    f.write(', '.join(ignore_value_keys))
    f = open(report_name + '.ignore_value_keys_fuzzy', 'w+')
    f.write(', '.join(ignore_value_keys_fuzzy))

    #case本身错误，直接返回错误
    if not online_status :
        return json.loads(onlinedata)
    if not test_status:
        return json.loads(offlinedata)
    #比较返回的数据
    quick_mode = True
    return compareResult(onlinedata, offlinedata, ignore_value_keys, ignore_value_keys_fuzzy, ignore_key_keys, quick_mode, ignore_all_value_mode)