# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from nose.tools import *
from baas.core.plugins import PluginLoader

pluginXmmp = PluginLoader()
pluginXmmp.load_plugins()
pluginXmmp.load_map()
pluginXmmp.load_help()
pluginXmmp.load_limits()

pluginWave = PluginLoader(format="wave")
pluginWave.load_plugins()
pluginWave.load_map()
pluginWave.load_help()
pluginWave.load_limits()

pluginRaw = PluginLoader(format="raw")
pluginRaw.load_plugins()
pluginRaw.load_map()
pluginRaw.load_help()
pluginRaw.load_limits()

def test_xmmp_handler():   
    assert_true(len(pluginXmmp.plugins) > 1, 'no plugins loaded, xmpp (default) mode')    

def test_wave_handler():   
    assert_true(len(pluginWave.plugins) > 1, 'no plugins loaded, wave mode')

def test_raw_handler():   
    assert_true(len(pluginWave.plugins) > 1, 'no plugins loaded, raw mode')
