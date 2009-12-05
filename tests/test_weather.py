# -*- coding: utf-8 -*-
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

xmmp = pluginXmmp.plugins.get('Weather')
wave = pluginWave.plugins.get('Weather')

def test_xmmp_forecast():
    result = xmmp.forecast('moscow #ru')   
    assert_true(re.search(r'Влажность:', result.encode('utf-8')), 'No forecast found')

def test_wave_forecast():   
    result = wave.forecast('köln #de'.decode('utf-8')) 
    assert_true(re.match(r'^ <br/><br/><b>Cologne, NRW</b>', result), 'No forecast title found')
    assert_true(re.search(r'Feuchtigkeit:', result), 'No forecast found')
