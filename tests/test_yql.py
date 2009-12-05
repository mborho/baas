# -*- coding: utf-8 -*-
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

newsXmmp = pluginXmmp.plugins.get('Yql')
newsWave = pluginWave.plugins.get('Yql')

#tests for web search
def test_xmmp_web():   
    result = newsXmmp.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'\(20', result), 'no result date found')    

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