# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
#from nose.tools import *
#from tests import pluginWave, pluginXmmp, pluginRaw
#import re

#newsXmmp = pluginXmmp.plugins.get('Yql')
#newsWave = pluginWave.plugins.get('Yql')
#raw = pluginRaw.plugins.get('Yql')

# test result size limits
#def test_limits():    
    #assert_equal(10, raw.result_limit,  'result size incorrect')    
    #assert_equal(pluginRaw.limits['news'], raw.result_limit ,'result_size for news incorrect')        
    #assert_equal(pluginRaw.limits['web'], raw.result_limit ,'result_size for web incorrect')        
    #assert_equal(pluginRaw.limits['blip'], raw.result_limit ,'result_size for blip incorrect')        
    
#def test_xmmp_limits():   
    ## test several page params
    #result0 = newsXmmp.search_web('%s #de [0]' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"Searching the web for d\xfcsseldorf", result0), 'no result title found')    
    #assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result0), 'no result found')    
    
    #result1 = newsXmmp.search_web('%s [1] #de ' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"Searching the web for d\xfcsseldorf", result1), 'no result title found')    
    #assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result0), 'no result found')    
    #assert_equal(result0, result1, 'first page invalid')    
    
    #result2 = newsXmmp.search_web('%s #de [2]' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"Searching the web for d\xfcsseldorf", result2),  'no result title found')    
    #assert_not_equal(result0, result2, 'no second page')    
    
    #resultNone = newsXmmp.search_web('%s #de []' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"Searching the web for d\xfcsseldorf", resultNone), 'no result title found')    
    #assert_not_equal(result0, resultNone, 'not default first page') 
    
##tests for web search
#def test_xmmp_web():   
    #result = newsXmmp.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"Searching the web for d\xfcsseldorf", result), 'no result title found')    
    #assert_true(re.search(r'\(20', result), 'no result date found')  
    
    #result1 = newsXmmp.search_web('%s #de [2]' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"Searching the web for d\xfcsseldorf", result1), 'no result title found') 
    #assert_not_equal(result, result1, 'second page invalid')  

#def test_wave_web():   
    #result = newsWave.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    #assert_true(re.search(r"<br/><br/><b>Searching the web for d\xfcsseldorf", result), 
        #'no result title found')    
    #assert_true(re.search(r'</b><br/><a href="http://www.duesseldorf.de/">', result),
        #'no result found')
   