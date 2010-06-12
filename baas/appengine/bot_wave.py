#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import ConfigParser
from waveapi import events
from waveapi import robot 
from waveapi import appengine_robot_runner
from baas.core.plugins import PluginLoader
from baas.core.helpers import *

config = ConfigParser.ConfigParser()
config.read("../../baas.cfg")

pluginHnd = PluginLoader(config=config, format="wave")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()
commands= pluginHnd.commands

def OnRobotAdded(event, wavelet):
    """Invoked when the robot has been added."""
    reply = "type 'buddy:help' for available commands"
    wavelet.reply(reply)

def OnBlipSubmitted(event, wavelet):
    blip = event.blip
    text = blip.text.strip()
    reply = ''
    if text and text == 'buddy:help':
        help = "\n\n%s" % pluginHnd.help
        blip.append(help)
    elif text and text.find(':')+1:
        cmd,args=text.split(':',1)
        commando_func = commands.get(cmd)
        if commando_func:
            result_msg = commando_func(args)
            reply = result_msg
    
    if reply != '':
        blip.all().delete()        
        reply = '<b>asked</b> %s %s' % (xmlify(text), reply)
        blip.append_markup(reply)

if __name__ == '__main__':
    myRobot = robot.Robot(config.get('wave','name'),
        image_url=config.get('wave','image_url'),
        profile_url=config.get('wave','profile_url'))
    myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)
    myRobot.register_handler(events.BlipSubmitted, OnBlipSubmitted)
    appengine_robot_runner.run(myRobot)
