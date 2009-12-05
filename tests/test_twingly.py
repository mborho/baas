# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

xmmp = pluginXmmp.plugins.get('Twingly')
wave = pluginWave.plugins.get('Twingly')

#tests for blogs
def test_xmmp_blogs():   
    result = xmmp.blogs('düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"blog search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'\* ', result), 'no result found')    

def test_wave_blogs():   
    result = wave.blogs('düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"<br/><br/><b>blog search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'<a href="http://', result),
        'no result found')

#tests for microblogs
def test_xmmp_micro():   
    result = xmmp.microblogs('düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"microblog search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'\* ', result), 'no result found')      

def test_wave_micro():   
    result = wave.microblogs('düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"<br/><br/><b>microblog search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'<a href="http://twitter.com', result),
        'no result found')