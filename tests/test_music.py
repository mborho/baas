# -*- coding: utf-8 -*-
# Copyright 2010 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp, pluginRaw
import re

xmmp = pluginXmmp.plugins.get('Music')
wave = pluginWave.plugins.get('Music')
raw = pluginRaw.plugins.get('Music')

# test result size limits
def test_limits():    
    assert_equal(10, raw.result_limit,  'result size incorrect')    
    for cmd in pluginRaw.limits:
        if cmd not in  ['music']: continue
        assert_equal(pluginRaw.limits[cmd], raw.result_limit ,'result_size for %s incorrect' % cmd)        
    
#tests for web search
def test_xmmp_music():   
    result = xmmp.search('%s' % 'slayer')    
    assert_true(re.search(r"Searching artists for slayer", result), 'no result title found')    
    assert_true(re.search(r'new.music.yahoo.com/slayer/', result), 'no result found')    

def test_xmmp_music_single():   
    result = xmmp.search('%s' % 'hell awaits')    
    assert_true(re.search(r"Searching artists for hell awaits", result), 'no result title found')    
    assert_true(re.search(r'new.music.yahoo.com/hell-awaits/', result), 'no result found')    
    
def test_xmmp_music_release():   
    result = xmmp.search('%s #release' % 'meantime')
    assert_true(re.search(r"Searching releases for meantime", result), 'no result title found')    
    assert_true(re.search(r'"Meantime" \(1992\) by Helmet', result), 'no result found')   

def test_xmmp_music_track():   
    result = xmmp.search('%s #track' % 'hell awaits')    
    assert_true(re.search(r"Searching tracks for hell awaits", result), 'no result title found')    
    assert_true(re.search(r'"Hell Awaits" \(1993\) by Slayer', result), 'no result found')   
    
def test_xmmp_limits():   
    # test several page params
    result0 = xmmp.search('%s [0]' % 'summer')
    assert_true(re.search(r"Searching artists for summer", result0), 'no result title found')    
    assert_true(re.search(r'Donna Summer', result0), 'no result found')    
    
    result1 = xmmp.search('%s [1]' % 'summer')
    assert_true(re.search(r"Searching artists for summer", result1), 'no result title found')    
    assert_true(re.search(r'Donna Summer', result1), 'no result found')    
    assert_equal(result0, result1, 'first page invalid')    
    
    result2 = xmmp.search('%s [2]' % 'summer')
    assert_true(re.search(r"Searching artists for summer", result2), 'no result title found')    
    assert_not_equal(result0, result2, 'no second page')    
    
    resultNone = xmmp.search('%s []' % 'summer')
    assert_true(re.search(r"Searching artists for summer", resultNone), 'no result title found')    
    assert_not_equal(result0, resultNone, 'not default first page') 

def test_wave_music():   
    result = wave.search('%s #track' % 'Köln'.decode('utf-8'))    
    assert_true(re.search(r"<br/><br/><b>Searching tracks for K\xf6ln", result), 
        'no result title found')    
    assert_true(re.search(r'>K\xf6ln</a> \(1995\)', result),
        'no result found')

     