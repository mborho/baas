# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp, pluginRaw
import re

xmmp = pluginXmmp.plugins.get('Maemo')
wave = pluginWave.plugins.get('Maemo')
raw = pluginRaw.plugins.get('Maemo')

# test result size limits
def test_limits():    
    assert_equal(8, raw.result_limit,  'result size incorrect')    
    for cmd in pluginRaw.limits:
        if cmd != 'tmo': continue
        assert_equal(pluginRaw.limits[cmd], raw.result_limit ,'result_size for %s incorrect' % cmd)        
    
#tests for web search
def test_xmmp_talk():   
    result = xmmp.talk('Nitdroid')    
    assert_true(re.search(r'talk.maemo.org hits for Nitdroid', result), 
        'no result title found')    
    assert_true(re.search(r'Android', result), 'no result found')    

def test_xmmp_limits():   
    # test several page params
    result0 = xmmp.talk('Nitdroid') 
    assert_true(re.search(r'talk.maemo.org hits for Nitdroid', result0), 'no result title found')    
    assert_true(re.search(r'Android', result0), 'no result found')    
    
    result1 = xmmp.talk('Nitdroid [1]')    
    assert_true(re.search(r'talk.maemo.org hits for Nitdroid', result1), 'no result title found')    
    assert_true(re.search(r'NITDroid', result1), 'no result found')    
    assert_equal(result0, result1, 'first page invalid')    
    
    result2 = xmmp.talk('Nitdroid [2]')    
    assert_true(re.search(r'talk.maemo.org hits for Nitdroid', result2), 'no result title found')    
    assert_not_equal(result0, result2, 'no second page')    
    
    resultNone = xmmp.talk('Nitdroid []')    
    assert_true(re.search(r'talk.maemo.org hits for Nitdroid', resultNone), 'no result title found')    
    assert_not_equal(result0, resultNone, 'not default first page') 

def test_wave_talk():   
    result = wave.talk('Nitdroid')    
    assert_true(re.search(r'<br/><br/><b>talk.maemo.org hits for Nitdroid', result), 
        'no result title found')    
    assert_true(re.search(r'<br/><a href="http://talk.maemo.org/showthread.php', result),
        'no result found')    
        
        
def test_xmmp_wiki():   
    result = xmmp.wiki('Kernel')    
    assert_true(re.search(r'wiki.maemo.org hits for Kernel', result), 
        'no result title found')    
    assert_true(re.search(r'Kernel Power', result), 'no result found')    
    
    
def test_xmmp_packages():   
    result = xmmp.packages('Ziggy')    
    assert_true(re.search(r'Maemo packages for Ziggy', result), 
        'no result title found')    
    assert_true(re.search(r'Ask Ziggy', result), 'no result found')        