# -*- coding: utf-8 -*-
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

xmmp = pluginXmmp.plugins.get('Delicious')
wave = pluginWave.plugins.get('Delicious')

#tests for bookmarks
def test_xmmp_deli():   
    result = xmmp.bookmarks('%s' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"Bookmarks for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'\(20', result), 'no result date fund')    

def test_wave_deli():   
    result = wave.bookmarks('%s' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"<br/><br/><b>Bookmarks for d\xfcsseldorf", result), 
        'no result title fund')    
    assert_true(re.search(r' \(20', result), 'no result date fund')

#tests for popular bookmarks
def test_xmmp_deli_pop():   
    result = xmmp.bookmarks('%s #pop' % 'wave'.decode('utf-8')) 
    assert_true(re.search(r"Bookmarks for wave", result), 'no result title found')    
    assert_true(re.search(r'http://completewaveguide.com/', result), 'no pop link found')    

def test_wave_deli_pop():   
    result = wave.bookmarks('%s #pop' % 'wave'.decode('utf-8')) 
    assert_true(re.search(r"<br/><br/><b>Bookmarks for wave", result), 'no result title fund')    
    assert_true(re.search(r'href="http://completewaveguide.com/"', result), 'no pop link found')    