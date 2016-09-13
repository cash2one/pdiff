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
import os
import time



"""
比较两个Json字符串
ignore_value_keys: 数组，比较json时，不比较数组中key对应的Value，关于这个key的修改不放到比较结果中
ignore_key_keys:数组，比较json时，忽略数组中的key，关于这个key的删、改都不放到比较结果中。
"""
def compareResult(online="1", offline="1"):
    diff_res = {
		    u"_update":{},
		    u"_append":{}
	}
    old = float(online)
    new = float(offline)
    perf = float("%.2f"%(((new - old)/old)*100))
    if perf > 5:
	    diff_res["_update"]["perf"] = perf
	    return diff_res["_update"]
    else:
	    diff_res["_append"]["perf"] = perf
	    return diff_res["_append"]
    
def getAvg(datas):
    data_sorted = sorted(datas)
    lenth = len(datas)
    if lenth > 2:
        #去掉最大值和最小值
        sumdata = sum(datas) - data_sorted[lenth-1] - data_sorted[0]
        #计算平均值
        avg = sumdata/(lenth-2)
    else:
        avg = sum(datas)/lenth
    #avg = 0
    #for i in range(1, lenth):
        #avg += (datas[i-1] - avg)/i
    return str(avg)

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
    conn = httplib.HTTPConnection(hosturl)
    #请求URL
    try:
        conn.request(httpMethod, path, params, headers)
        response = conn.getresponse()
        if not response.status == 200 :
            onlinedata = '{"error" : "server +' + server_description + ' return status code is' + response.status + '"}'
            requestResult = False
        else:
            onlinedata = response.getheader("total")
    except:
        onlinedata = '{"error" : "server ' + server_description + ' is not available"}'
        requestResult = False
    conn.close()
    return requestResult, onlinedata

def runTest(executor, testcase, testtarget, testcookie, report_folder=config.PDIFF_CONFIG['report_folder']):
	
    #设置执行机配置的UA、Refer、Cookies
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    headers['Referer'] = executor.referer
    headers['User-Agent'] = executor.ua
    headers['Cookie'] = ''
    for cookie in executor.cookies:
        headers['Cookie'] += cookie[0].upper() + '=' + cookie[1] + ';'
    #获取需要run的URL
    url = getRealTestUrl(testcase, executor)
    
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
    #请求测试环境
    #设置连接的Host, 如果testtarget未指定port，从配置中替换url
    if testtarget == 'ONLINE':
        testtarget=o.netloc
    elif ':' not in testtarget:
        testurl = config.URL_REPLACE[o.netloc]
        testtarget = testurl.replace('HOST', testtarget)
    
    #添加测试环境自定义cookie
    headers['Cookie'] = headers['Cookie'] + testcookie + ';'
    headers['Cookie'] = headers['Cookie'] + '__perf=qatest' + ';'
    #请求测试URL
    datas=[]
    for i in range(1, 50):
    	(test_status, offlinedata) = request(testtarget, httpMethod, o.path + '?' + o.query, o.params, headers, report_name , 'TEST')
	if i > 39:
		datas.append(int(offlinedata))

    offlinedata = getAvg(datas)
    #比较返回的数据
    filename = report_name +  '.perf'
    if os.path.exists(filename):
	    f = open(filename, "r")
	    onlinedata = f.read()
	    f.close()
	    os.rename(filename,filename+".old")

	    f = open(filename+".new", "w+")
	    f.write(offlinedata)
	    f.close()
	    return compareResult(onlinedata, offlinedata)
    else:
	    f = open(filename, "w+")
	    f.write(offlinedata)
	    f.close()
    return compareResult() 
