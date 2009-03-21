# -*- coding: utf-8 -*-
import re
from urllib import quote_plus
from util import text, console
from yos.yql import db, udfs
from baas.core.plugins import Plugin

REDDIT_LINK_REGEX = re.compile(r'<a href="(?P<url>[^\"]*?)">\[link\]</a>')

class Masher (Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('hot',self.combine_hot)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
    
        return {
            'commands': ['hot:tech - scratches hot news from various sources'],
            'additional': [],
        }

    def normalize_ycomb(self, row):
        '''
            normalizes ycombinator results
        '''
        result = {}
        result['title'] = row['y$title']
        result['link'] = row['y$link']
        return result

    def normalize_reddit(self, row):
        '''
            normalizes ycombinator results
        '''
        result = {}
        result['title'] = row['r$title']
        result['link'] = self.grep_reddit_link(row['r$description'])
        return result

    def grep_reddit_link(self, desc):
        '''
            grabs link out if reddit description 
        '''
        m = REDDIT_LINK_REGEX.search(desc)
        #print m.groups()
        if not m: return ''
        return m.group('url')

    def normalize_deli(self, row):
        '''
            normalizes ycombinator results
        '''
        result = {}
        #print row
        result['title'] = row['d$title']
        result['link'] = row['d$link']
        return result
   
    def combine_hot(self, what):
        '''
        combines popular links from varoius news sites
        '''
        if what == '':
            return "Which hotness do you mean?"

        result = ''
        pages = None
        if what == "tech":
            # thanks, http://lethain.com/entry/2008/jul/12/stripping-reddit-from-hackernews-with-boss-mashup/
            ycomb = db.create(name="y",url="http://news.ycombinator.com/rss")
            _ycomb = db.select(udf=udfs.unnest_value,table=ycomb)
            _ycomb = db.select(udf=self.normalize_ycomb,table=_ycomb)
            #print _ycomb.rows[0]
            #print __ycomb.rows[0]

            #reddit = db.create(name="r",url="http://www.reddit.com/.rss")
            #_reddit = db.select(udf=udfs.unnest_value,table=reddit)
            #_reddit = db.select(udf=self.normalize_reddit,table=_reddit)
            #print _reddit.rows[0:2]
            #print __reddit.rows[0:2]

            deli = db.create(name="d",url="http://feeds.delicious.com/v2/rss/?count=50")
            _deli = db.select(udf=udfs.unnest_value,table=deli)
            _deli = db.select(udf=self.normalize_deli,table=_deli)
            #print _deli.rows[0:2]

            pages = db.join(self.overlap_link, [_ycomb, _deli])

        if pages:
            result = 'Hot %s news' % what
            for row in pages.rows:
                result += '%s - %s\n' % (row["y$title"], row["d$link"])

        return result