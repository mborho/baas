# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
from baas.core.bossapi import BossApi
from baas.core.plugins import Plugin

class Boss (Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('news',self.search_news), ('web', self.search_web), ('blip',self.search_blip)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        additional = '''
Some commands (news,web) can be combined with #de, examples:
news:hamburg #de
web:xmpp #de'''

        return {
            'commands': ['news:word - searches for news','web:word - websearch','blip:song - search for songs on blip.fm'],
            'additional': [additional],
        }

    def search_web(self, term):
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

        yterm = term.encode('utf-8')
        
        boss_api = BossApi(self.config.get('boss','api_key'))#,logging)
        response = boss_api.web(query=yterm,count=10, lang=lang, region=lang)
        hits = response.get('resultset_web')

        result = 'Searching the web for "%s"\n' % term
        if hits:
            for row in hits:
                result += "(%s) %s : %s\n" % (row['date'],row['title'],row['url'])
        else:
            result += 'No sites found!'
        return self.strip_tags(result)

    def search_news(self, term):
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

        yterm = term.encode('utf-8')

        boss_api = BossApi(self.config.get('boss','api_key'))#,logging)
        response = boss_api.news(query=yterm,count=10, lang=lang, region=lang)
        hits = response.get('resultset_news')

        result = 'Searching news for "%s"\n' % term
        if hits:
            for row in hits:
                result += "(%s) %s : %s\n" % (row['date'],row['title'],row['url'])
        else:
            result += 'No news found!'
        return self.strip_tags(result)

    def search_blip(self, term):
        '''
        searches for blips on blip.fm
        '''
        term = term.strip()

        if term == '':
            return "Please specify your search term"
        
        term_utf8 = term.encode('utf-8')
        yterm = 'intitle:%s site:blip.fm inurl:profile -intitle:"Props given" -intitle:"Favourite DJs" \
                -intitle:"Blip.fm %s"' % (term_utf8, term_utf8)

        boss_api = BossApi(self.config.get('boss','api_key'))#,logging)
        response = boss_api.web(query=yterm,count=15)
        hits = response.get('resultset_web')

        result = 'Blips for "%s"\n' % term
        if hits:
            for row in hits:
                result += "%s : %s\n" % (row['title'].replace('Blip.fm | ',''),row['url'])
        else:
            result += 'No blips found!'
        return self.strip_tags(result)

