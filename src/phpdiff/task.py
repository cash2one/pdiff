# coding=utf-8

'''
Created on 2013年10月25日

@author: liwei06
'''

import os

class TaskDescription :

    taskDescription=''
    casebucketName=''
    executorName=''
    tag=''

    def get_task_description(self):
        return self.taskDescription

    def get_casebucket_name(self):
        return self.casebucketName

    def get_executor_name(self):
        return self.executorName
        
    def get_tag(self):
        return self.tag


    def __init__(self, taskStr=''):
        if taskStr.strip()!= '' and taskStr.strip()!='\n' and taskStr.strip()!='\r\n':
            if taskStr[-1] == '\n':
                taskStr = taskStr[:-1]
            if taskStr[-1] == '\r':
                taskStr = taskStr[:-1]
#             taskStr = taskStr.decode('utf-8')
            taskSplits = taskStr.split('\t')
            if(len(taskSplits) >= 4):
                self.taskDescription=taskSplits[0]
                self.casebucketName=taskSplits[1]
                self.tag=taskSplits[2]
                self.executorName=taskSplits[3]
                

class Task:
    taskDescription=''
    caselist=[]
    executor=''
    
    def __init__(self, taskDescription, caselist, executor):
        self.taskDescription = taskDescription
        self.caselist = caselist
        self.executor = executor
    
def loadTasks(taskfile, casebucketMap, executorMap):
    tasklist = []
    if os.path.isfile(taskfile):
        fh = open(taskfile)
        for line in  fh.readlines():
            
            if line.strip()== '' and line.strip()=='\n' and line.strip()=='\r\n':
                continue
            print 'task:' + line
            taskDes = TaskDescription(line)
            
            description = taskDes.get_task_description()
            tag = taskDes.get_tag()
            buketname = taskDes.get_casebucket_name()
            
            if taskDes.get_tag().upper()=='ALL':
                cases = casebucketMap[buketname].get_caselist()
            else:
                cases = casebucketMap[buketname].get_caselist_by_tag(tag)
            
            executor = executorMap[taskDes.get_executor_name()]
            tasklist.append(Task(description, cases, executor))

    print 'loaded ' + str(len(tasklist)) + ' tasks from ' +  taskfile
    return tasklist
            
            
    