#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import traceback
import ConfigParser
from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish, xmlstream
from twisted.internet import reactor
from baas.plugins import help, doomicile, boss

########################### helpers ##############################################
def getTraceback():
    e_info = sys.exc_info()
    e_tb   = "".join(traceback.format_tb(e_info[2]))
    return ' Error Type: '+str(e_info[0])+'\nError Value: '+str(e_info[1])+'\nTraceback:\n'+e_tb+'\n'

commands={
    #'s': boss.Boss().search,
    'help': help.Help().man,
    'web': boss.Boss().search_web,
    'news': boss.Boss().search_news,
    'bm': doomicile.Doomicile().search_bookmarks,
}

class Bot(object):

    def __init__(self, config):

        self.config = config
        self.debug = self.config.getint('app','debug')
        
        me = jid.JID(self.config.get('bot','jid'))
        self.factory = client.basicClientFactory(me, self.config.get('bot','pwd'))
        self.factory.addBootstrap('//event/stream/authd',self.authd)
        self.factory.addBootstrap(client.BasicAuthenticator.AUTH_FAILED_EVENT, self.authfailedEvent)

        reactor.connectTCP(self.config.get('bot','server'), self.config.getint('bot','port'), self.factory)
        
        reactor.run()
        self.reactor = reactor

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


        reply = "type 'help:list' for available commands"

        try:
            if text and text.find(':')+1:
                cmd,args=text.split(':',1)
                commando_func = commands.get(cmd)
                if commando_func:
                    result_msg = commando_func(args)
                    #print result_msg
                    reply = result_msg
                else:
                    reply = 'Uups, commando not known\n'
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
        print "authd"
        # need to send presence so clients know we're
        # actually online.
        presence = domish.Element(('jabber:client', 'presence'))
        presence.addElement('status').addContent('Online')

        xmlstream.send(presence)

        # add a callback for the messages
        xmlstream.addObserver('/message', self.gotMessage)
        self.xmlstream = xmlstream

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("baas.cfg")
    bot = Bot(config)