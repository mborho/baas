# -*- coding: utf-8 -*-
from urllib import quote_plus
from yos.yql import db, udfs
from baas.core.plugins import Plugin

class Doomicile(Plugin):

    def get_map(self):
        cmd_map = [('bm',self.search_bookmarks)]
        return cmd_map

    def get_help(self):
        return {'commands':['bm:tag - searches bm.doomicile'],'additional':[]}

    def search_bookmarks(self, term):
        '''
        searches web by yahoo
        '''
        result = ''
        term = term.strip()
        if term == '':
            return "Please specify your search term"

        #bm = db.select(name="bm", udf=udfs.unnest_value, url="http://feeds.delicious.com/rss/popular/"+quote_plus(term))
        bm = db.select(name="bm", udf=udfs.unnest_value, url="http://bm.doomicile.de/rss/all/"+quote_plus(term))
        #table = db.create(data=dl)

        result = 'Searching bookmarks for "%s"\n' % term
        if bm.rows:
            for row in bm.rows[0:5]:
                desc = row["bm$description"]+"\n" if len(row["bm$description"]) > 0 else ''
                result += '%s\n%s\n%s\n' % (row["bm$title"], row["bm$link"], desc)
                #result += '%s\n%s\n%s\n\n' % (row["bm$title"], row["bm$link"], row["bm$subject"])
        else:
            result += 'No sites found!'
        return self.strip_tags(result)



if __name__ == "__main__":
    import sys
    print Doomicile().search_bookmarks(sys.argv[1])
