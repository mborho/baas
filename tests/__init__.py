# -*- coding: utf-8 -*-
from nose.tools import *
from baas.core.plugins import PluginLoader

pluginXmmp = PluginLoader()
pluginXmmp.load_plugins()
pluginXmmp.load_map()
pluginXmmp.load_help()

pluginWave = PluginLoader(format="wave")
pluginWave.load_plugins()
pluginWave.load_map()
pluginWave.load_help()

def test_xmmp_handler():   
    assert_true(len(pluginXmmp.plugins) > 1, 'no plugins loaded, wave mode')    

def test_wave_handler():   
    assert_true(len(pluginWave.plugins) > 1, 'no plugins loaded, wave mode')
