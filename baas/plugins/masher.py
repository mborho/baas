# -*- coding: utf-8 -*-
import re
from urllib import quote_plus
from util import text, console
from yos.yql import db, udfs
from yos.boss import ysearch
from baas.core.plugins import Plugin

REDDIT_LINK_REGEX = re.compile(r'<a href="(?P<url>[^\"]*?)">\[link\]</a>')

class Masher (Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [
            ('hot', self.combine_hot),
            ('popnews', self.rank_news_by_social)
        ]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
    
        return {
            'commands': [
                'hot:links - looks up what\'s hot on reddit and delicious',
                'popnews:word - popular ranked news for searchterm',
            ],
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
        if not m: return ''
        return m.group('url')

    def normalize_deli(self, row):
        '''
            normalizes ycombinator results
        '''
        result = {}
        result['title'] = row['d$title']
        result['link'] = row['d$link']
        return result
   
    def combine_hot(self, what):
        '''
        combines popular links from varoius news sites
        '''
        if what == '':
            return "Which hotness do you mean?"

        pages = None
        if what == "links":
            # thanks, http://lethain.com/entry/2008/jul/12/stripping-reddit-from-hackernews-with-boss-mashup/
            ycomb = db.create(name="y",url="http://news.ycombinator.com/rss")
            _ycomb = db.select(udf=udfs.unnest_value,table=ycomb)
            _ycomb = db.select(udf=self.normalize_ycomb,table=_ycomb)

            reddit = db.create(name="r",url="http://www.reddit.com/.rss?limit=50")
            _reddit = db.select(udf=udfs.unnest_value,table=reddit)
            _reddit = db.select(udf=self.normalize_reddit,table=_reddit)

            #deli = db.create(name="d",url="http://feeds.delicious.com/v2/rss/?count=50")
            #_deli = db.select(udf=udfs.unnest_value,table=deli)
            #_deli = db.select(udf=self.normalize_deli,table=_deli)

            pages = db.join(self.overlap_link, [_reddit, _ycomb])
        

            result = 'Hot %s\n' % what
            if pages:
                for row in pages.rows:
                    result += '%s - %s\n' % (row["y$title"], row["y$link"])
            else:
                result += 'No sites found!'
        else:
            result = "Function not implemented by now"
        return result

    def socialf(self, row):
        #row.update({"social": row["dg$diggs"] + row["yt$favorites"]}) ; return row
        row.update({"social": row["dg$diggs"]}) ; return row

    def rank_news_by_social(self, term):
        '''
            example 4 of the YMF Examples
        '''
        term = term.strip()
        if term == '':
            return "Please specify your search term"

        ynews_data = ysearch.search(term, vertical="news", count=100, more={"news.ranking": "date"})
        ynews = db.create(name="ynews", data=ynews_data)
        ynews.rename(before="headline", after="title")

        smf = lambda r: {"title": r["title"]["value"]}
        sm = db.select(name="sm", udf=smf, url="http://search.twitter.com/search.atom?lang=en&q="+quote_plus(term)+"&rpp=60")
        #sm.rename(before="text", after="title")

        #ytf = lambda r: {"title": r["title"]["value"], "favorites": int(r["statistics"]["favoriteCount"])}
        #yt = db.select(name="yt", udf=ytf, url="http://gdata.youtube.com/feeds/api/videos?vq="+quote_plus(term)+"&lr=en&orderby=published")

        diggf = lambda r: {"title": r["title"]["value"], "diggs": int(r["diggCount"]["value"])}
        digg = db.select(name="dg", udf=diggf, url="http://digg.com/rss_search?search="+quote_plus(term)+"&area=dig&type=both&section=news")

        tb = db.join(self.overlap_title, [ynews, sm, digg])#, yt])

        tb = db.select(udf=self.socialf, table=tb)
        tb = db.group(by=["ynews$title"], key="social", reducer=lambda d1,d2: d1+d2, as="rank", table=tb, norm=text.norm)
        tb = db.sort(key="rank", table=tb)

        result = 'Popular news for "%s"\n' % term
        if tb.rows:
            for row in tb.rows:
                result += '(%s) %s %s (%d)\n' % (row['ynews$date'], row["ynews$title"], row["ynews$url"], row['rank'])
        else:
            result = 'No sites found!'

        return result