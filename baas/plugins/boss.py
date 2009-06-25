# -*- coding: utf-8 -*-

from urllib import quote_plus
from util import text, console
from yos.boss import ysearch
from yos.yql import db, udfs
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

        data = ysearch.search(term,count=10,lang=lang,region=lang)
        table = db.create(data=data)

        result = 'Searching the web for "%s"\n' % term
        if table.rows:
            for row in table.rows:
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

        data = ysearch.search(term, vertical="news", count=10,lang=lang,region=lang)#1, more={'sort':'date'})
        table = db.create(data=data)

        result = 'Searching news for "%s"\n' % term
        if table.rows:
            for row in table.rows:
                #print row
                result += "(%s) %s : %s\n" % (row['date'],row['title'],row['url'])
        else:
            result += 'No sites found!'
        return self.strip_tags(result)

    def search_blip(self, term):
        '''
        searches for blips on blip.fm
        '''
        term = term.strip()

        if term == '':
            return "Please specify your search term"
        
        yterm = 'intitle:%s site:%s' % (term.encode('utf-8'), 'blip.fm')
        data = ysearch.search(yterm,count=10)
        table = db.create(data=data)

        result = 'Blips for "%s"\n' % term
        if table.rows:
            for row in table.rows:
                result += "%s : %s\n" % (row['title'].replace('Blip.fm | ',''),row['url'])
        else:
            result += 'No blips found!'
        return self.strip_tags(result)
        
    def search_news_delicious(self, term):
        '''
        searches yahoo news and delicious popular links for gioven search term
        '''
        term = term.strip()
        if term == '':
            return "Please specify your search term"

        dl = db.select(name="dl", udf=udfs.unnest_value, url="http://feeds.delicious.com/rss/popular/"+quote_plus(term))
        #dl.describe()
        yn = db.create(name="yn", data=ysearch.search(term, vertical="news", count=50))

        tb = db.join(self.overlap_predicate, [dl, yn])
        tb = db.group(by=["yn$title"], key=None, reducer=lambda x,y: None, as=None, table=tb, norm=text.norm)

        result = 'Searching news for "%s"\n' % term
        if tb.rows:
            for row in tb.rows:
                result += '%s\n%s\n' % (row["yn$title"], row["dl$link"])
        else:
            result += 'No sites found!'
            
        return result

