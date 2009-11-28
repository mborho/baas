# -*- coding: utf-8 -*-
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re
newsXmmp = pluginXmmp.plugins.get('Yql')
newsWave = pluginWave.plugins.get('Yql')

#print news.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))
#print news.search_news('%s #de' % 'düsseldorf'.decode('utf-8'))
#print news.search_blip('%s' % 'metallica'.decode('utf-8'))

def test_xmmp_web():   
    result = newsXmmp.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Searching the web for d\xfcsseldorf", result), 
        'no result title fund')    
    assert_true(re.search(r'\(20', result), 'no result date fund')    

def test_wave_web():   
    result = newsWave.search_web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"<br/><br/><b>Searching the web for d\xfcsseldorf", result), 
        'no result title fund')    
    assert_true(re.search(r'</b><br/><a href="http://www.duesseldorf.de/">', result),
        'no result found')
