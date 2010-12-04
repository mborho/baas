# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp, pluginRaw
import re

xmmp = pluginXmmp.plugins.get('Gsearch')
wave = pluginWave.plugins.get('Gsearch')
raw = pluginRaw.plugins.get('Gsearch')

# test result size limits
def test_limits():    
    assert_equal(8, raw.result_limit,  'result size incorrect')    
    for cmd in pluginRaw.limits:
        if cmd not in  ['gnews','wikipedia','wiktionary','gweb','metacritic','imdb']: continue
        assert_equal(pluginRaw.limits[cmd], raw.result_limit ,'result_size for %s incorrect' % cmd)        
    
#tests for web search
def test_xmmp_gweb():   
    result = xmmp.web('%s #de' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Web search for d\xfcsseldorf", result), 
        'no result title found')    
    assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result), 'no result found')    

def test_xmmp_limits():   
    # test several page params
    result0 = xmmp.web('%s #de [0]' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"Web search for d\xfcsseldorf", result0), 'no result title found')    
    assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result0), 'no result found')    
    
    result1 = xmmp.web('%s [1] #de ' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Web search for d\xfcsseldorf", result1), 'no result title found')    
    assert_true(re.search(r'Landeshauptstadt D\xfcsseldorf', result1), 'no result found')    
    assert_equal(result0, result1, 'first page invalid')    
    
    result2 = xmmp.web('%s #de [2]' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Web search for d\xfcsseldorf", result2), 'no result title found')    
    assert_not_equal(result0, result2, 'no second page')    
    
    resultNone = xmmp.web('%s #de []' % 'düsseldorf'.decode('utf-8'))    
    assert_true(re.search(r"Web search for d\xfcsseldorf", resultNone), 'no result title found')    
    assert_not_equal(result0, resultNone, 'not default first page') 

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

    result1 = xmmp.news('%s #de [2]' % 'düsseldorf'.decode('utf-8')) 
    assert_true(re.search(r"Google news search for d\xfcsseldorf", result), 'no result title found') 
    assert_not_equal(result, result1, 'second page invalid')    
    

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
    assert_true(re.search(r'Halo 3', result),
        'no result found')

#tests for imdb
def test_xmmp_imdb():   
    result = xmmp.imdb('Bastards #en') 
    assert_true(re.search(r'Results on IMDb for "Bastards"', result), 'no result title found') 
    assert_true(re.search(r'Bastards of the Party \(2005\)', result), 'no hit found')
    assert_true(re.search(r'http://', result), 'no result link found')  
    
    result1 = xmmp.imdb('Bastards #en [3]') 
    assert_true(re.search(r'Results on IMDb for "Bastards"', result1), 'no result title found') 
    assert_not_equal(result, result1, 'third page invalid')    

def test_wave_imdb():   
    result = wave.imdb('%s #de' % 'Köln'.decode('utf-8')) 
    assert_true(re.search(r'<br/><br/><b>Results on IMDb for "K\xf6ln"', result), 
        'no result title found')    
    assert_true(re.search(r'>"SOKO K\xf6ln"', result),'no result found')

#tests for wikipedia
def test_xmmp_wpedia():   
    result = xmmp.wikipedia('Madrid #es') 
    assert_true(re.search(r'Wikipedia entries for "Madrid"', result), 'no result title found') 
    assert_true(re.search(r'Madrid - Wikipedia, la enciclopedia libre', result), 'no hit found')
    assert_true(re.search(r'http://', result), 'no result link found')        

def test_wave_wpedia():   
    result = wave.wikipedia('%s #de' % 'Köln'.decode('utf-8')) 
    assert_true(re.search(r'<br/><br/><b>Wikipedia entries for "K\xf6ln"', result), 
        'no result title found')    
    assert_true(re.search(r'http://de.wikipedia.org/wiki/', result),'no result found')
    
    result1 = wave.wikipedia('%s #de [2]' % 'Köln'.decode('utf-8')) 
    assert_true(re.search(r'<br/><br/><b>Wikipedia entries for "K\xf6ln"', result1), 
        'no result title found')    
    assert_not_equal(result, result1, 'second page invalid')   

#tests for wiktionary
def test_xmmp_wiktionary():   
    result = xmmp.wiktionary('Saucisse #fr') 
    assert_true(re.search(r'Wiktionary entries for "Saucisse"', result), 'no result title found') 
    assert_true(re.search(r'Wiktionnaire - Wikipedia, la enciclopedia libr', result), 'no hit found')
    assert_true(re.search(r'http://', result), 'no result link found')        

def test_wave_wiktionary():   
    result = wave.wiktionary('%s #fr' % 'été'.decode('utf-8')) 
    assert_true(re.search(r'<br/><br/><b>Wiktionary entries for "\xe9t\xe9"', result), 
        'no result title found')    
    assert_true(re.search(r'http://fr.wiktionary.org/wiki/', result),'no result found')
    
    result1 = wave.wiktionary('%s #fr [2]' % 'été'.decode('utf-8')) 
    assert_true(re.search(r'<br/><br/><b>Wiktionary entries for "\xe9t\xe9"', result1), 
        'no result title found')    
    assert_not_equal(result, result1, 'second page invalid')   


#tests for imdb
def test_xmmp_amazon():   
    result = xmmp.amazon('n900 #de') 
    assert_true(re.search(r'Products on Amazon for "n900"', result), 'no result title found') 
    assert_true(re.search(r'Nokia N900 Smartphone black: Amazon.de: Elektronik', result), 'no hit found')
    assert_true(re.search(r'http://', result), 'no result link found')  
    
    result1 = xmmp.amazon('n900 #de [2]') 
    assert_true(re.search(r'Products on Amazon for "n900"', result1), 'no result title found') 
    assert_false(re.search(r'Nokia N900 Smartphone black: Amazon.de: Elektronik', result1), 'no hit found')
    assert_not_equal(result, result1, 'second page invalid')        
