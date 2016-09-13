# coding=utf-8

'''
Created on 2013年12月2日

@author: liwei06
'''

import sys
import testcase
import executor
import task
import run_test

import config
import os
import time

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
t = time.time()
lt = time.localtime(t)
t_str = time.strftime('%Y%m%d%H%M%S',lt) + str(t)[-5:-3]
reportpath = config.PDIFF_CONFIG['report_folder']


if len(sys.argv) > 3:
    taskfile = sys.argv[1]
    testhost1 = sys.argv[2]
    testhost2 = sys.argv[3]
else:
    print 'tasklist and testhost should be specified '

if len(sys.argv) > 4 :
    testcookie = sys.argv[4]
    
    
cmap = testcase.load_casebucketMap( '../../case/');
executorMap = executor.load_executes('../../executor')
tasklist = task.loadTasks("../../task/" + taskfile + ".txt", cmap, executorMap)
    
testData = []
reportData = []
for mytask in tasklist:
    print 'handle task ' + mytask.taskDescription
    for case in mytask.caselist:
        print 'handle case ' + case.get_description()
        reportfolder = reportpath + '/' + taskfile + '_' + t_str + '/' + case.get_name() + '@' + mytask.executor.get_name()
        if not os.path.exists(reportfolder):
            os.makedirs(reportfolder)
            
        run_test.runDataTest(mytask.executor, case, testhost1, testhost2, testcookie, reportfolder)
        

