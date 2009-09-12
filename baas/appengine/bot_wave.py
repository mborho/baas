#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import ConfigParser
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi.ops import OpBuilder
from baas.core.plugins import PluginLoader
from baas.core.helpers import *

config = ConfigParser.ConfigParser()
config.read("../../baas.cfg")

pluginHnd = PluginLoader(config=config, format="wave")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()
commands= pluginHnd.commands


def OnRobotAdded(properties, context):
    """Invoked when the robot has been added."""
    reply = "type 'buddy:help' for available commands"
    root_wavelet = context.GetRootWavelet()
    root_wavelet.CreateBlip().GetDocument().SetText(reply)

def OnBlipSubmitted(properties, context):
    """ checks every new blip """
    blip = context.GetBlipById(properties['blipId'])
    text = blip.GetDocument().GetText().strip()

    reply = ''
    if text and text == 'buddy:help':
        help = "\n\n%s" % pluginHnd.help
        blip.GetDocument().SetText("%s\n%s" % (text, help))
    elif text and text.find(':')+1:
        cmd,args=text.split(':',1)
        commando_func = commands.get(cmd)
        if commando_func:
            result_msg = commando_func(args)
            reply = result_msg

    
    if reply != '':
        blip.GetDocument().SetText(" ")
        reply = '<b>asked</b> %s %s' % (xmlify(text), reply)
        builder = OpBuilder(context)
        builder.DocumentAppendMarkup(blip.waveId, blip.waveletId, properties['blipId'], reply)



if __name__ == '__main__':
    myRobot = robot.Robot(config.get('wave','name'),
        image_url=config.get('wave','image_url'),
        version=config.get('wave','version'),
        profile_url=config.get('wave','profile_url'))
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.Run()
