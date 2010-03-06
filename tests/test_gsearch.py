# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
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

#tests for metacric
def test_xmmp_metacritc():   
    result = xmmp.metacritic('it crowd') 
    assert_true(re.search(r'Reviews for "it crowd"', result), 'no result title found') 
    assert_true(re.search(r'http://', result), 'no result link found')    

def test_wave_metacritic():   
    result = wave.metacritic('halo') 
    assert_true(re.search(r'<br/><br/><b>Reviews for "halo"', result), 
        'no result title found')    
    assert_true(re.search(r'platforms/xbox360/halo3">Halo 3 \(xbox360\) reviews at Metacritic.com', result),
        'no result found')

#tests for imdb
def test_xmmp_imdb():   
    result = xmmp.imdb('Bastards #en') 
    assert_true(re.search(r'Results on IMDb for "Bastards"', result), 'no result title found') 
    assert_true(re.search(r'Bastards of the Party \(2005\)', result), 'no hit found')
    assert_true(re.search(r'http://', result), 'no result link found')    

def test_wave_imdb():   
    result = wave.imdb('%s #de' % 'Köln'.decode('utf-8')) 
    assert_true(re.search(r'<br/><br/><b>Results on IMDb for "K\xf6ln"', result), 
        'no result title found')    
    assert_true(re.search(r'>"SOKO K\xf6ln"', result),'no result found')
