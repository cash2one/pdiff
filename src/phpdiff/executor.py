# coding=utf-8
'''
Created on 2013年10月24日

@author: liwei06
'''

import ConfigParser
import os

class TestExecutor:

    defaultParameters = []
    
    def get_name(self):
        return self.name

    def get_method(self):
        return self.method

    def get_ua(self):
        return self.ua

    def get_referer(self):
        return self.refer

    def get_cookies(self):
        return self.cookies

    def get_default_parameters(self):
        return self.defaultParameters

    def set_method(self, value):
        self.method = value

    def set_ua(self, value):
        self.ua = value

    def set_referer(self, value):
        self.referer = value

    def set_cookies(self, value):
        self.cookies = value

    def set_default_parameters(self, value):
        self.defaultParameters = value

    def set_name(self, value):
        self.name = value
    
def load_executes(folder=''):
    
    executorsMap={}
    
    if folder!='':
        files = os.listdir(folder)
        for f in files:
            fulPath = folder + '/' + f;
            
            if os.path.isfile(fulPath):
                
                config = ConfigParser.RawConfigParser(allow_no_value=True)
                config.read(fulPath)
                executor=TestExecutor()
                executor.set_method(config.items('Method')[0][0])
                executor.set_ua(config.items('User-Agent')[0][0])
                executor.set_referer(config.items('Referer')[0][0])
                if f.endswith('.txt'):
                    f = f[:-4]
                executor.set_name(f)
                
                if config.has_section('Cookie'):
                    executor.set_cookies(config.items('Cookie'))
                
                if config.has_section('DefaultParameters'):
                    executor.set_default_parameters(config.items('DefaultParameters'))
                
                if f[-4:]=='.txt':
                    f=f[0:len(f)-4]
                    
                executorsMap[f]=executor
                
                print 'loaded executor ' + f + ' from: ' + fulPath
                
    return executorsMap
                    
                    
                    
            
