#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import sys
import os.path
import traceback
import ConfigParser
from optparse import OptionParser
from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish, xmlstream
from twisted.internet import reactor
from baas.core.plugins import PluginLoader

########################### helpers ##############################################
def getTraceback():
    e_info = sys.exc_info()
    e_tb   = "".join(traceback.format_tb(e_info[2]))
    return ' Error Type: '+str(e_info[0])+'\nError Value: '+str(e_info[1])+'\nTraceback:\n'+e_tb+'\n'

class Bot(object):

    def __init__(self, config, ):

        self.config = config
        self.debug = self.config.getint('app','debug')
        self._load_plugins()

        me = jid.JID(self.config.get('bot','jid'))
        self.factory = client.basicClientFactory(me, self.config.get('bot','pwd'))
        self.factory.addBootstrap('//event/stream/authd',self.authd)
        self.factory.addBootstrap(client.BasicAuthenticator.AUTH_FAILED_EVENT, self.authfailedEvent)

        reactor.connectTCP(self.config.get('bot','server'), self.config.getint('bot','port'), self.factory)
        
        reactor.run()
        self.reactor = reactor

    def _load_plugins(self):        
        self.pluginHnd = PluginLoader(config=self.config)
        self.pluginHnd.load_plugins()
        self.pluginHnd.load_map()
        self.pluginHnd.load_help()
        self.commands= self.pluginHnd.commands

    def gotMessage(self, message):
        
        if self.debug:
            print message.toXml()
        text = None
        user = message["from"]
        # sorry for the __str__(), makes unicode happy
        for e in message.elements():
            if e.name == "body":
                text = unicode(e.__str__())
                break

        reply = "type 'help' for available commands"

        try:

            if text and text.find(':')+1:
                cmd,args=text.split(':',1)
                commando_func = self.commands.get(cmd)
                if commando_func:
                    result_msg = commando_func(args)
                    reply = result_msg
                else:
                    reply = 'Uups, commando not known\n'
            elif text and text == 'help':
                reply += "\n\n%s" % self.pluginHnd.help

        except:
            reply = getTraceback()

        response = domish.Element((None, 'message'))
        response['to'] = user
        response["type"] = 'chat'
        response.addElement('body', content=reply)
        
        self.xmlstream.send(response)

    def authfailedEvent(self, xmlstream):
        global reactor
        try:
            self.reactor.stop()
        except:
            pass
        sys.exit('Auth failed!')
        

    def authd(self, xmlstream):
        # need to send presence so clients know we're
        # actually online.
        presence = domish.Element(('jabber:client', 'presence'))
        presence.addElement('status').addContent('Online')

        xmlstream.send(presence)

        # add a callback for the messages
        xmlstream.addObserver('/message', self.gotMessage)
        self.xmlstream = xmlstream

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-c", "--config", dest="config",
                      help="configuration file (default: /etc/baas.conf)")
    parser.add_option("-s", "--show-conf-example", dest="show_conf_example",
                     action="store_true", default=False, help="show example config file")
    (options, args) = parser.parse_args()

    
    if not options.config:
        config_file = "/etc/baas.conf"
    else:
        config_file = options.config

    if options.show_conf_example:
        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf/baas.conf'))
        conf_example = f.read()
        f.close()
        print conf_example
        sys.exit()
    elif not os.path.isfile(config_file):
        sys.exit('Configuration file does not exist, exiting. Type -h for help.')

    config = ConfigParser.ConfigParser()
    config.read(config_file)

    print "starting buddy as service bot"
    bot= Bot(config)

if __name__ == "__main__":
    main()

