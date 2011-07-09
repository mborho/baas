# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
from baas.core.yqlapi import YQLApi
from baas.core.plugins import Plugin
from baas.core.helpers import strip_tags, xmlify, htmlentities_decode

class Yql (Plugin):

    def __init__(self, config, format='xmpp'):
        super(Yql,self).__init__(config, format)
        self.result_limit = 10
        
    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = []#('web', self.search_web)]
        return cmd_map

    def get_limits(self):
        """
            returns the limit map for the plugin commands
        """
        limit_map = []#('web', self.result_limit)]            
        return limit_map
        
    def get_help(self):
        """
            returns the help text for the plugin
        """
        additional = '''Some commands (news,web) can be combined with lang-codes, like #de, #en, #es etc: web:xmpp #de'''

        return {
            'commands': [],#'web:word - websearch',
            'additional': [''],
        }

    def _get_offset(self, page):
        return (page-1)*self.result_limit
        
    def _extract_hits(self, result):
        hits = result.get('result') if result else None
    
        # handle single result
        if type(hits) == dict:
            hits = [hits]
        return hits
         
    def search_web(self, term):
        '''
        searches web by yahoo
        DEPRECATED
        '''
        term = term.strip()
        lang = None
        page = 1
        if term:
            (term, page) = self.extract_page_param(term)                            
            if term.find('#')+1:
                term, lang = term.split('#',1)
                term = term.strip()

        if term == '':
            return "Please specify your search term"

        # handle single and double quotes
        term = term.replace("'",'"')

        query = 'select title,url,date,abstract '
        query += 'from search.web(%d,%d) where query=\'%s\' ' % (self._get_offset(page), self.result_limit, term)

        if lang:
            query += ' AND region="%s" AND lang="%s" ' % (lang, lang)

        yql_api = YQLApi()
        response = yql_api.request(query=query)
        hits = self._extract_hits(response)
        
        title = 'Searching the web for %s\n' % term
        return self.render(data=hits, title=title)
        
    def render_xmpp(self, hits, title):
        '''
        renders the result for xmpp responses
        '''
        result = title+"\n"
        if hits:
            for row in hits:
                result += "(%s) %s : %s\n" % (row['date'],row['title'],row['url'])
        else:
            result += 'No hits found!'
        return strip_tags(result)

    def render_wave(self, hits, title):
        '''
        renders the result for wave responses
        '''
        result = " <br/><br/><b>%s</b><br/>" % xmlify(title)
        if hits:
            for row in hits:
                title = xmlify(row['title'])
                result += '<a href="%s">%s</a><br/><br/>' % (xmlify(row['url']), title)
        else:
            result += 'No hits found!'
        return result
