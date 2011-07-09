# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from tests import pluginWave, pluginXmmp
import re

xmmp = pluginXmmp.plugins.get('Translate')
wave = pluginWave.plugins.get('Translate')

#tests for german english
def test_xmmp_de_en():
    result = xmmp.translate('üben @de #en'.decode('utf-8'))   
    assert result == 'practice (de => en)'

def test_wave_de_en():   
    result = wave.translate('üben @de #en'.decode('utf-8')) 
    assert result == ' <br/><br/><b>practice</b> <i>(de =&gt; en)</i>'

#tests for german_spain
def test_xmmp_de_es():   
    result = xmmp.translate('üben @de #es'.decode('utf-8')) 
    assert result == 'práctica (de => es)'.decode('utf-8')  

def test_wave_de_es():   
    result = wave.translate('üben @de #es'.decode('utf-8')) 
    assert result == ' <br/><br/><b>práctica</b> <i>(de =&gt; es)</i>'.decode('utf-8')  