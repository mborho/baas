# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp

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
