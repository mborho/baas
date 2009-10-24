# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
from baas.core.yqlapi import YQLApi
from baas.core.plugins import Plugin

class Gsearch (Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('gnews',self.news), ('gweb', self.web)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        additional = '''gnews and gweb can be also combined with lang-codes, like #de, #en, #es etc:
gnews:hamburg #de
gweb:xmpp #de'''

        return {
            'commands': ['gnews:word - google news search','gweb:word - google web search'],
            'additional': [additional],
        }

    def _extract_hits(self, result):
        hits = result.get('results') if result else None
    
        # handle single result
        if type(hits) == dict:
            hits = [hits]
        return hits
         
    def web(self, term):
        '''
        searches web by yahoo
        '''
        term = term.strip()
        lang = None

        if term and term.find('#')+1:
            term, lang = term.split('#',1)
            term = term.strip()

        if term == '':
            return "Please specify your search term"

        query = 'select * from google.search(0,8) where q="%s"' % term
        if lang:
            query += ' AND gl="%s"' % (lang)

        yql_api = YQLApi(community=True)
        response = yql_api.request(query=query)
        hits = self._extract_hits(response)

        title = 'Web search for %s\n' % term
        return self.render(data=hits, title=title)

    def news(self, term):
        '''
        searches news
        '''
        term = term.strip()
        lang = None

        if term and term.find('#')+1:
            term, lang = term.split('#',1)
            term = term.strip()

        if term == '':
            return "Please specify your search term"

        query = 'USE "http://www.datatables.org/google/google.news.xml" AS google.news; '  
        query += 'select * from google.news(0,8) where q="%s"' % term
        if lang:
            query += ' AND ned="%s"' % (lang)

        yql_api = YQLApi(community=True)
        response = yql_api.request(query=query)
        hits = self._extract_hits(response)

        title = 'Google news search for %s\n' % term
        return self.render(data=hits, title=title)        
        
    def render_xmpp(self, hits, title):
        '''
        renders the result for xmpp responses
        '''
        result = title+"\n"
        if hits:
            for row in hits:
                title = row['titleNoFormatting']
                if row.get('publisher'):
                    title = "%s: %s" % (row.get('publisher'), title)
                result += "%s - %s\n" % (self.htmlentities_decode(title), row['unescapedUrl'])
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
                title = row['titleNoFormatting']
                if row.get('publisher'):
                    title = "%s: %s" % (row.get('publisher'), title)
                title = self.xmlify(self.htmlentities_decode(title))
                result += '<a href="%s">%s</a><br/><br/>' % (self.xmlify(row['url']), title)
        else:
            result += 'No hits found!'
        return result