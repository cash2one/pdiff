# coding=utf-8

'''
Created on 2013年10月29日

@author: liwei06
'''

# if __name__ == '__main__':

import sys
import pytest
import testcase
import executor
import task
import run_test

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
        print 'handle task ' + mytask.taskDescription
        for case in mytask.caselist:
            print 'handle case ' + case.get_description()
            report_folder= reportpath + '/' + taskfile + '_' + t_str + '/' + case.get_name() + '@' + mytask.executor.get_name()
            report_data_suitename = mytask.taskDescription
            report_data_casename =  case.get_description()
            report_data_caseid = case.get_caseid()
            report_data_host = testhost + ':' + testcookie
            report_data_author = case.get_author()
            report_data_url = testhostsrc
            if testhostsrc == 'ONLINE':
                report_data_url = run_test.getRealTestUrl(case, mytask.executor)
            
            report_date_jsonDiffPath = config.PDIFF_CONFIG['report_platform'] +"task=" + taskfile + '_' + t_str + "&" + "case=" + case.get_name() + '@' + mytask.executor.get_name()             
            testData.append([mytask.executor, case, testhost, testcookie, testhostsrc, report_folder])   
            reportData.append("#".join([report_data_suitename,report_data_casename,report_data_author,report_data_host,report_data_url,report_date_jsonDiffPath,str(report_data_caseid)]))

            
     
#     with open('testlog','w') as f:
#         #pickle.dump(testData[0][6].decode('utf-8'), f)
#         for debugDate in reportData:
#             f.write(debugDate)
#             f.write("###\r\n")
#               
            
        
    metafunc.parametrize(["testExecutor", "case", "testHost", "testCookie", "testHostSrc", "reportFolder"], testData,False,reportData)
    


def test_pdiff(testExecutor, case, testHost, testCookie, testHostSrc,reportFolder):
    
    if not os.path.exists(reportFolder):
        os.makedirs(reportFolder)
    result = run_test.runTest(testExecutor, case, testHost, testCookie, testHostSrc, reportFolder)
    retrytime = 3
    print 'retrytime1:', retrytime
    #add retry logic
    while retrytime >0 and len(result)!=0:
        result = run_test.runTest(testExecutor, case, testHost, testCookie, testHostSrc, reportFolder)
        retrytime = retrytime -1
        print 'retrytime2:', retrytime
        time.sleep(0.3)
    assert len(result)==0
    

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
t = time.time()
lt = time.localtime(t)
t_str = time.strftime('%Y%m%d%H%M%S',lt) + str(t)[-5:-3]
reportpath = config.PDIFF_CONFIG['report_folder']
testhostsrc = 'ONLINE'
testcookie = 'pub_env=1'

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
if len(sys.argv) > 6 :
    testhostsrc = sys.argv[6]
if __name__ == '__main__':

	junitPath = config.PDIFF_CONFIG['report_folder'] + '/' + taskfile + '_' + t_str
	if not os.path.exists(junitPath):
   		os.makedirs(junitPath)
	pytest.main('./phpdiff.py -v --junitxml_pdiff='+config.PDIFF_CONFIG['report_folder'] + '/' + taskfile + '_' + t_str + '/result.xml')
	
	#pytest.main('./phpdiff.py  -p junitxml_pdiff --junitxml_pdiff=./result.xml')
	# pytest_generate_tests('');
