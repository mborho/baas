# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
from baas.core.yqlapi import YQLApi
from baas.core.plugins import Plugin
from baas.core.helpers import format_pub_date

class Delicious (Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('deli',self.bookmarks),]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        return {
            'commands': ['deli:tag [#pop] - tag search on delicious.com. Ordered by date, with #pop ordered by popularity'],           
        }

    def bookmarks(self, term):
    
        term = term.strip()
        order = None
        
        if term and term.find('#')+1:
            term, order = term.split('#',1)
            term = term.strip()
            
        if term == '':
            return "Please specify your url to lookup"
            
        table = 'delicious.feeds'
        if order == "pop":
            table += '.popular'

        query = 'select * from %s where tag="%s" limit 10' % (table, term)

        yql_api = YQLApi(community=True)
        response =yql_api.request(query)        
        hits = response.get('item') if response else None
        return self.render(data=hits, title='Bookmarks for %s:' % term)        
        
    def render_xmpp(self, hits, title):
        '''
        renders the result for xmpp responses
        '''
        result = title+"\n"
        if hits:
            for row in hits:               
                result += "(%s) %s : %s\n" % (format_pub_date(row['pubDate'],'%Y/%m/%d'), row['title'],row['link'])
        else:
            result += 'No hits found!'
        return self.strip_tags(result)

    def render_wave(self, hits, title):
        '''
        renders the result for wave responses
        '''
        result = " <br/><br/><b>%s</b><br/>" % self.xmlify(title)
        if hits:
            for row in hits:
                title = self.xmlify(row['title'])
                result += '<a href="%s">%s (%s)</a><br/><br/>' % (self.xmlify(row['link']), title,\
                format_pub_date(row['pubDate'],'%Y/%m/%d'))
        else:
            result += 'No hits found!'
        return result      
