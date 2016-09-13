# coding=utf-8

'''
Created on 2013年10月24日

@author: liwei06
'''

import os


class Testcase: 
    
    #按照字符串去加载case内容
    def __init__(self, caseStr='', name='000', id = 0):
        
        print 'loading case: ' + caseStr + '; name is ' + name 
        if caseStr.strip()!= '' and caseStr.strip()!='\n' and caseStr.strip()!='\r\n':
            if caseStr[-1] == '\n':
                caseStr = caseStr[:-1]
            if caseStr[-1] == '\r':
                caseStr = caseStr[:-1]
                
#             caseStr = caseStr.decode('utf-8')
            caseSplits = caseStr.split('\t')
            
            if(len(caseSplits) >= 7):
                
                self.description = caseSplits[0];
                self.author = caseSplits[1];
                self.method = caseSplits[2];
                self.url = caseSplits[3];
                self.parameters = caseSplits[4];
                ignores = caseSplits[5];
                self.tag = caseSplits[6];
                self.caseid = id
                self.name=name
                 
                if len(ignores) == 0:
                    print  'the case load ignore key fail!!!, content is :' + caseStr
                
                if(ignores[0] == '[' and ignores[-1] == ']'):
                    self.ignoreKeys = ignores[1:len(ignores)-1].split(',');
                    
                else:
                    print 'the case load ignore key fail!!!, content is :' + caseStr
            
            else:
                print 'the case load fail!!! the content is : ' + caseStr

    def get_description(self):
        return self.description


    def get_author(self):
        return self.author


    def get_url(self):
        return self.url


    def get_parameters(self):
        return self.parameters


    def get_ignore_keys(self):
        return self.ignoreKeys


    def get_tag(self):
        return self.tag


    def get_name(self):
        return self.name


    def get_method(self):
        return self.method
    
    def get_caseid(self):
        return self.caseid
class TestCaseBucket:
    
    #按指定目录去加载case
    def __init__(self, folder=''):
        self.caselist = []
        if folder != '':
            files = os.listdir(folder)
            self.bucketname = os.path.basename(folder)
            for f in files:
                fulPath = folder + '/' + f;
                if os.path.isfile(fulPath):
                    num = 0
                    fh = open(fulPath)
                    for line in  fh.readlines():
                        #generate case id
                        if line.strip()!= '' and line.strip()!='\n' and line.strip()!='\r\n':
                            casename=str(num)
                            while len(casename) < 3:
                                casename = '0' + casename
                            if f.endswith('.txt'):
                                f = f[:-4]
                            casename = self.bucketname + '.' + f + casename
                                
                            case = Testcase(line, casename,num)
                            self.caselist.append(case)
                            num = num + 1
                        
                    print 'loaded ' + str(num) + ' cases in: ' +  fulPath
        return 
    
    def get_caselist(self):
        return self.caselist
    
    def get_caselist_by_tag(self, tag):
        
        caselistbypriority = []
        
        for case in self.caselist:
            if case.get_tag() == tag:
                caselistbypriority.append(case)

        return caselistbypriority

def load_casebucketMap(folder=''):
        
        bucketMap = {}
        
        if folder != '':
            files = os.listdir(folder)
            for f in files:
                fulPath = folder + f;
                if os.path.isdir(fulPath):
                    print 'loading case bucket: ' + f + ', from ' + fulPath
                    bucket = TestCaseBucket(fulPath);
                    bucketMap[bucket.bucketname] = bucket
        return bucketMap
    
    
    