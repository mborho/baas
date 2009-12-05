# -*- coding: utf-8 -*-
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

xmmp = pluginXmmp.plugins.get('Gsearch')
wave = pluginWave.plugins.get('Gsearch')

#tests for web search
def test_xmmp_gweb():   
    result = xmmp.web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Web search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result), 'no result found')    

def test_wave_gweb():   
    result = wave.web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"<br/><br/><b>Web search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'</b><br/><a href="http://www.duesseldorf.de/">', result),
        'no result found')

#tests for news search
def test_xmmp_gnews():   
    result = xmmp.news('%s #de' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"Google news search for d\xfcsseldorf", result), 'no result title found') 
    assert_true(re.search(r'http://', result), 'no result link found')    

def test_wave_gnews():   
    result = wave.news('%s #de' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"<br/><br/><b>Google news search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'">[^<]*D\xfcsseldorf[^<]*</a>', result),
        'no result found')