#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import logging
import ConfigParser
from baas.core.plugins import PluginLoader
from baas.core.helpers import *
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

config = ConfigParser.ConfigParser()
config.read("../../baas.cfg")

pluginHnd = PluginLoader(config=config)
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()
commands= pluginHnd.commands

class XMPPHandler(webapp.RequestHandler):

    def post(self):
        
        message = xmpp.Message(self.request.POST)
        # message.from,to,body,stanza
        text = message.body.strip()

        reply = "type 'help' for available commands"

        try:

            if text and text.find(':')+1:
                cmd,args=text.split(':',1)
                commando_func = commands.get(cmd)
                if commando_func:
                    result_msg = commando_func(args)
                    reply = result_msg
                else:
                    reply = 'Uups, commando not known\n'
            elif text and text == 'help':
                reply += "\n\n%s" % pluginHnd.help

        except Exception, e:
            logging.exception(e)
            reply = "An error occured, sorry"

        message.reply(reply)


application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
