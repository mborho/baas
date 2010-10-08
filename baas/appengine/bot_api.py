#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import logging
import ConfigParser
from urllib import unquote, quote
from baas.core.plugins import PluginLoader
from baas.core.helpers import *
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

logging.getLogger().setLevel(logging.DEBUG)

config = ConfigParser.ConfigParser()
config.read("../../baas.cfg")

pluginHnd = PluginLoader(config=config,format="raw")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()
commands= pluginHnd.commands

class QueryHandler(webapp.RequestHandler):

    def get(self):
        term = self.request.get('term')
        json_callback = self.request.get('jsoncallback')
        json_mime = self.request.get('json', True)
        reply = ''
        try:
            if term and term.find(':')+1:
                cmd,args=term.split(':',1)
                commando_func = commands.get(cmd)
                if commando_func:
                    result_msg = commando_func(args)
                    reply = result_msg
                else:
                    reply = '{"error":"service unknown"}'
            elif term and term == 'help':
                reply += '{"help":pluginHnd.help}'
            else:
                reply = '{"error":"service unknown"}'
        except Exception, e:
            logging.exception(e)
            reply = '{"error":"%s"}' % quote(unicode(e))
        
        if json_mime:
            self.response.headers['Content-Type'] = 'application/json charset=utf-8'
        self.response.out.write('%s (%s)' % (json_callback, simplejson.dumps(reply))) 

class ServicesHandler(webapp.RequestHandler):

    def get(self):
        logging.info(commands.keys())
        if self.request.get('json', True):
            self.response.headers['Content-Type'] = 'application/json charset=utf-8'
        self.response.out.write(simplejson.dumps(commands.keys()))
        
application = webapp.WSGIApplication([
                ('/api/query',QueryHandler),
                ('/api/services', ServicesHandler),    
                ],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
