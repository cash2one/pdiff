# coding=utf-8

'''
Created on 2013年10月29日

'''

#if __name__ == '__main__':

import sys
import pytest
import testcase
import executor
import task
import run_perftest
import config
import os
import time



taskfile=''
testhost=''
testcookie=''
reportpath= ''

def pytest_generate_tests(metafunc):
    
    cmap = testcase.load_casebucketMap( '../../case/');
    executorMap = executor.load_executes('../../executor')
    tasklist = task.loadTasks("../../task/" + taskfile + ".txt", cmap, executorMap)
    
    testData = []
    reportData = []
    for mytask in tasklist:
        for case in mytask.caselist:
            report_folder= reportpath + '/' + taskfile + '_' + t_str + '/' + case.get_name() + '@' + mytask.executor.get_name()
            report_data_suitename = mytask.taskDescription
            report_data_casename =  case.get_description()
            report_data_host = testhost + ':' + testcookie
            report_data_author = case.get_author()
            report_data_url = report_folder + "/" + case.get_name() + '@' + mytask.executor.get_name() 
	    report_date_jsonDiffPath = "perf"
            testData.append([mytask.executor, case, testhost, testcookie, report_folder]) 
            reportData.append("|".join([report_data_suitename,report_data_casename,report_data_author,report_data_host,report_data_url,report_date_jsonDiffPath]))
    
    metafunc.parametrize(["testExecutor", "case", "testHost", "testCookie", "reportFolder"], testData,False,reportData)
    


def test_pdiff(testExecutor, case, testHost, testCookie, reportFolder):
    
    if not os.path.exists(reportFolder):
        os.makedirs(reportFolder)
     
    result = run_perftest.runTest(testExecutor, case, testHost, testCookie, reportFolder)
    #retrytime = 3
    #add retry logic
    #while retrytime >0 and len(result)!=0:
    #result = run_perftest.runTest(testExecutor, case, testHost, testCookie, reportFolder)
    #retrytime = retrytime -1
    
    assert 0 == result['perf']
    

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
t = time.time()
lt = time.localtime(t)
t_str = time.strftime('%Y%m%d%H%M%S',lt) + str(t)[-5:-3]
reportpath = config.PDIFF_CONFIG['report_folder']

if len(sys.argv) > 2:
    taskfile = sys.argv[1]
    testhost = sys.argv[2]
else:
    print 'tasklist and testhost should be specified '

if len(sys.argv) > 3 :
    testcookie = sys.argv[3]
  
if len(sys.argv) > 4 :    
    t_str = sys.argv[4]
    
if len(sys.argv) > 5 :
    reportpath = sys.argv[5]
if __name__ == '__main__':
    junitPath = reportpath +'/' + taskfile + '_' + t_str
    if not os.path.exists(junitPath):
        os.makedirs(junitPath)
    pytest.main( './perfdiff.py -v  --junitxml_pdiff='+junitPath+'/result.xml')
