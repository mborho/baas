# -*- coding: utf-8 -*-
from urllib import quote_plus
from yos.yql import db, udfs
from baas.core.plugins import Plugin

class Twingly(Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('blog',self.blogs), ('micro',self.microblogs)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        return {'commands':['blog:word - blog search via twingly','micro:word - microblog search via twingly'],'additional':[]}

    def _search(self, term, content):

        term = term.strip()
        if term == '':
            return "Please specify your search term"

        twingly_rss = "http://www.twingly.com/search.rss?q=%s&sort=published&content=%s"  % (quote_plus(term.encode('utf-8')), content)
        items = db.select(name="bm", udf=udfs.unnest_value, url=twingly_rss)
        result = '%s search for "%s"\n' % (content, term)
        if items.rows:
            for row in items.rows[0:5]:
                desc = row["bm$description"]+"\n" if len(row["bm$description"]) > 0 else ''
                result += '* %s' % row["bm$title"]
                if desc != '' and content== 'blog':
                    result += ': %s' % desc
                result += ' %s\n' % row["bm$link"]
            #result = result.replace('&hellip;','...')
            result = self.htmlentities_decode(result)
        else:
            result += 'No sites found!'

        return result

    def blogs(self, term):
        '''
        blog search
        '''
        result = self._search(term, 'blog')
        return self.strip_tags(result)


    def microblogs(self, term):
        '''
        microblog search
        '''
        result = self._search(term, 'microblog')
        return self.strip_tags(result)

