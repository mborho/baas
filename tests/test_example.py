# -*- coding: utf-8 -*-
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

xmmp = pluginXmmp.plugins.get('Example')
wave = pluginWave.plugins.get('Example')

def test_xmmp_example():   
    result = xmmp.example_action('foo')    
    assert result == "bla"

    result = xmmp.example_action('bla') 
    assert result == "I don't understand...?"

def test_wave_example():   
    result = wave.example_action('foo') 
    assert result == ' <br/><br/><b>bla</b>'

    result = wave.example_action('bla')   
    assert result == " <br/><br/><b>I don't understand...?</b>"
