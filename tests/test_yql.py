# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp, pluginRaw
import re

newsXmmp = pluginXmmp.plugins.get('Yql')
newsWave = pluginWave.plugins.get('Yql')
raw = pluginRaw.plugins.get('Yql')

# test result size limits
def test_limits():    
    assert_equal(10, raw.result_limit,  'result size incorrect')    
    assert_equal(pluginRaw.limits['news'], raw.result_limit ,'result_size for news incorrect')        
    assert_equal(pluginRaw.limits['web'], raw.result_limit ,'result_size for web incorrect')        
    assert_equal(pluginRaw.limits['blip'], raw.result_limit ,'result_size for blip incorrect')        
    
def test_xmmp_limits():   
    # test several page params
    result0 = newsXmmp.search_web('%s #de [0]' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result0), 'no result title found')    
    assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result0), 'no result found')    
    
    result1 = newsXmmp.search_web('%s #de [1]' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result1), 'no result title found')    
    assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result0), 'no result found')    
    assert_equal(result0, result1, 'first page invalid')    
    
    result2 = newsXmmp.search_web('%s #de [2]' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result2),  'no result title found')    
    assert_not_equal(result0, result2, 'no second page')    
    
    resultNone = newsXmmp.search_web('%s #de []' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", resultNone), 'no result title found')    
    assert_not_equal(result0, resultNone, 'not default first page') 
    
#tests for web search
def test_xmmp_web():   
    result = newsXmmp.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result), 'no result title found')    
    assert_true(re.search(r'\(20', result), 'no result date found')  
    
    result1 = newsXmmp.search_web('%s #de [2]' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result1), 'no result title found') 
    assert_not_equal(result, result1, 'second page invalid')  

def test_wave_web():   
    result = newsWave.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"<br/><br/><b>Searching the web for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'</b><br/><a href="http://www.duesseldorf.de/">', result),
        'no result found')

#tests for news search
def test_xmmp_news():   
    result = newsXmmp.search_news('%s #de' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"D\xfcsseldorf", result), 'no result found')    
    assert_true(re.search(r'\(20', result), 'no result date found')    
    
    result1 = newsXmmp.search_news('%s #de [3]' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"D\xfcsseldorf", result1), 'no result found')    
    assert_not_equal(result, result1, 'third page invalid')  

def test_wave_news():   
    result = newsWave.search_news('%s #de' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"<br/><br/><b>Searching news for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'">[^<]*D\xfcsseldorf[^<]*</a>', result),
        'no result found')

#tests for blip.fm search
def test_xmmp_blip():   
    result = newsXmmp.search_blip('grönemeyer'.decode('utf-8')) 
    assert_true(re.search(r"Herbert Gr\xf6nemeyer", result), 'no result found')    
    assert_true(re.search(r'blip\.fm/profile/', result), 'no result link found')    

def test_wave_blip():   
    result = newsWave.search_blip('grönemeyer'.decode('utf-8')) 
    assert_true(re.search(r"<br/><br/><b>Blips for gr\xf6nemeyer", result), 
        'no result title found')    
    assert_true(re.search(r'">[^<]*Herbert Gr\xf6nemeyer[^<]*</a>', result),
        'no result found')
        
    result1 = newsWave.search_blip('grönemeyer [2]'.decode('utf-8')) 
    assert_true(re.search(r"<br/><br/><b>Blips for gr\xf6nemeyer", result1), 
        'no result title found')    
    assert_not_equal(result, result1, 'second page invalid')          