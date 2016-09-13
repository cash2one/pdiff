# -*- coding: utf-8 -*-
""" report test results in JUnit-XML format, for use with Hudson and build integration servers.

Based on initial code from Ross Lawley.
"""

import py
#import os
import re
import sys
import time
#import string
# import pickle


# Python 2.X and 3.X compatibility
try:
    unichr(65)
except NameError:
    unichr = chr
try:
    unicode('A')
except NameError:
    unicode = str
try:
    long(1)
except NameError:
    long = int


class Junit(py.xml.Namespace):
    pass


class TestCaseDetail(object):
    def __init__(self,report):
        names = report.nodeid.decode('utf-8').split("::")
        #names = report.nodeid.split("::")[1]
        #reportInfo = report.nodeid.decode('utf-8')
        reportInfo = self._get_report_data(names[-1])
        #reportInfo = names.split('[')[1].lstrip(']').split('|')

        self.suitename=reportInfo[0].lstrip('[')
        self.casename=reportInfo[1]
        self.author=reportInfo[2]
        self.host = reportInfo[3]
        self.url=reportInfo[4]
        self.jsonDiffPath=reportInfo[5]

        
    def _get_report_data(self, name):
        reportInfo = name[len(name.split('[')[0]):]
        if reportInfo[-1] == ']' :
            reportInfo = reportInfo[:-1]
        reportInfo = reportInfo.split('#')
        return reportInfo   
            
        
class TestNumbers(object):
    def __init__(self,passed=0,failures=0,errors=0,skipped=0):
        self.passed=passed
        self.failures=failures
        self.errors=errors
        self.skipped=skipped
    
    def add(self,variable,number=1):
        if variable in [ 'passed','failures','errors','skipped' ]:
            presentCounts=getattr(self,variable)
            setattr(self,variable,number+presentCounts)
        else:
            raise Exception("Wrong Test Number Type")
        
        
class TestCase(object):
    def __init__(self,result,detail,message,time=0):       
        self.detail=detail
	#changed by xiwu
	if message is None:
		self.message = "0"
	else:
		self.message=str(message.reprcrash)
	#changed by xiwu
        self.time=time
        
        self.testNumbers=TestNumbers()
        if result == 'pass':
            self.testNumbers.add('passed')
        elif result == 'failure':
            self.testNumbers.add('failures')            
        elif result == 'error':
            self.testNumbers.add('errors')
        elif result == 'skip':
            self.testNumbers.add('skipped')
        else:
            raise Exception("Wrong Test Result Type")
                                                    
class TestSuit(object):
    def __init__(self,name):
        self.name=name
        self.passed=0
        self.failures=0
        self.errors=0
        self.skipped=0
        self.time=0
           
    def addCase(self,testCase):
        if not hasattr(self,'testCases'):
            self.testCases=[]
                    
        self.testCases.append(testCase)
        self.passed += testCase.testNumbers.passed
        self.failures += testCase.testNumbers.failures
        self.errors += testCase.testNumbers.errors
        self.skipped += testCase.testNumbers.skipped
        self.time += testCase.time
    
                
                
# We need to get the subset of the invalid unicode ranges according to
# XML 1.0 which are valid in this python build.  Hence we calculate
# this dynamically instead of hardcoding it.  The spec range of valid
# chars is: Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD]
#                    | [#x10000-#x10FFFF]
_legal_chars = (0x09, 0x0A, 0x0d)
_legal_ranges = (
    (0x20, 0x7E),
    (0x80, 0xD7FF),
    (0xE000, 0xFFFD),
    (0x10000, 0x10FFFF),
)
_legal_xml_re = [unicode("%s-%s") % (unichr(low), unichr(high))
                  for (low, high) in _legal_ranges
                  if low < sys.maxunicode]
_legal_xml_re = [unichr(x) for x in _legal_chars] + _legal_xml_re
illegal_xml_re = re.compile(unicode('[^%s]') %
                            unicode('').join(_legal_xml_re))
del _legal_chars
del _legal_ranges
del _legal_xml_re

def bin_xml_escape(arg):
    def repl(matchobj):
        i = ord(matchobj.group())
        if i <= 0xFF:
            return unicode('#x%02X') % i
        else:
            return unicode('#x%04X') % i
    return py.xml.raw(illegal_xml_re.sub(repl, py.xml.escape(arg)))

def mangle_testnames(names):
    names = [x.replace(".py", "") for x in names if x != '()']
    names[0] = names[0].replace("/", '.')
    return names
    

def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption('--junitxml_pdiff', '--junit-xml_pdiff', action="store",
           dest="xmlpath", metavar="path", default=None,
           help="create junit-xml style report file at given path.")
               
def pytest_configure(config):
    xmlpath = config.option.xmlpath
    if xmlpath:
        config._xml = JunitReport(xmlpath)
        config.pluginmanager.register(config._xml)

def pytest_unconfigure(config):
    xml = getattr(config, '_xml', None)
    if xml:
        del config._xml
        config.pluginmanager.unregister(xml)
                
class JunitReport(object):
    def __init__(self,path):
        self.path=path        
        self.testSuits=[]
        self.passed = self.failures = self.errors = self.skipped = 0       
        
        
        
    def generateTestSuitXmls(self):        
        self.testSuitXmls = []
        for testSuit in self.testSuits:
            testCaseXmls = []           
            self.passed += testSuit.passed                                                          
            self.failures += testSuit.failures    
            self.errors += testSuit.errors
            self.skipped += testSuit.skipped
            
            for testCase in testSuit.testCases:
                
                if testCase.testNumbers.passed == 1:
                    extraMessageXml = Junit.passed(message = testCase.detail.url)
                elif testCase.testNumbers.failures == 1:
                    extraMessageXml = Junit.failure(message =  testCase.detail.url)
                elif testCase.testNumbers.skipped == 1:
                    extraMessageXml = Junit.skipped(message = testCase.detail.url)
                else:
                    extraMessageXml = Junit.error(message = testCase.detail.url)
                #add by xiwu 
		if testCase.detail.jsonDiffPath == "perf":
			if testCase.message == "0":
				message = testCase.message
			else:
				msg = testCase.message.split(":")
				info = msg[-1]
				perf = info.split(" ")
				message = perf[-1]
			extraMessageXml.append(message+"%")
		else:
			extraMessageXml.append(testCase.detail.jsonDiffPath)
                #add by xiwu
                
                testCaseXmls.append(Junit.testcase(
                                                   extraMessageXml,
                                                   name = bin_xml_escape(testCase.detail.casename),
                                                   author = testCase.detail.author,
                                                   url = bin_xml_escape(testCase.detail.url),
                                                   host = testCase.detail.host,
  
                                                                                                      
                                                   passed = testCase.testNumbers.passed,
                                                   failues = testCase.testNumbers.failures,
                                                   errors = testCase.testNumbers.errors,
                                                   skipped = testCase.testNumbers.skipped,                                                
                                                   time = testCase.time                                                  
                                                  )                                   
                                    )
                testCaseXmls.append("\n")
                                                     
            if len(testCaseXmls) != 0:                                                                                                    
                self.testSuitXmls.append(Junit.testsuite(
                                                        testCaseXmls,
                                                        name = testSuit.name,
                                                        count = testSuit.passed + testSuit.failures + testSuit.errors + testSuit.skipped,
                                                        passed = testSuit.passed,                                                          
                                                        failues = testSuit.failures,
                                                        errors = testSuit.errors,
                                                        skipped = testSuit.skipped,
                                                        time = testSuit.time                               
                                                        )                                     
                                         )
                self.testSuitXmls.append("\n")  
        return self.testSuitXmls           

                                          
                
    def pytest_sessionstart(self, session):
        self.suite_start_time = time.time()

    def pytest_runtest_logreport(self, report):
        testCaseDetail = TestCaseDetail(report)       
        time=getattr(report, 'duration', 0)                     
        if report.passed:
            if report.when == "call": # ignore setup/tear_down
                theTestCase = TestCase('pass',testCaseDetail,report.longrepr,time)
        elif report.failed:
            if report.when != "call":
                theTestCase = TestCase('error',testCaseDetail,report.longrepr,time)
            else:
                theTestCase = TestCase('failure',testCaseDetail,report.longrepr,time)
        elif report.skipped:
            theTestCase = TestCase('skip',testCaseDetail,report.longrepr,time)
         
        if 'theTestCase' in locals():            
            matchTestSuitList = [ testSuit for testSuit in  self.testSuits if testCaseDetail.suitename == testSuit.name]   
            if len(matchTestSuitList) == 0:
                theTestSuit = TestSuit(testCaseDetail.suitename)        
                self.testSuits.append(theTestSuit)
            else:
                theTestSuit = matchTestSuitList[0]
                
            theTestSuit.addCase(theTestCase)   
    
    def pytest_internalerror(self, excrepr):
        #待处理
        pass
                                                    
                
    def pytest_sessionfinish(self, session, exitstatus, __multicall__):
        if py.std.sys.version_info[0] < 3:
            logfile = py.std.codecs.open(self.path, 'w', encoding='utf-8')
        else:
            logfile = open(self.path, 'w', encoding='utf-8')
        
        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time
        theTestSuitXmls=self.generateTestSuitXmls()
             
        logfile.write('<?xml version="1.0" encoding="utf-8"?>\n')                        
        logfile.write(Junit.testsuites(                                                                                      
                                        '\n',                             
                                        theTestSuitXmls,
                                        name="TiebaPiffTest",
                                        count = self.passed + self.failures + self.errors + self.skipped,
                                        passed = self.passed,                                                          
                                        failues = self.failures,
                                        errors = self.errors,
                                        skipped = self.skipped,
                                          
                                        time="%.3f" % suite_time_delta,
                                        ).unicode(indent=0))       
        logfile.close()

            
            
