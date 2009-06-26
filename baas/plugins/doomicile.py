# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
from yos.yql import db, udfs
from baas.core.plugins import Plugin

class Doomicile(Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('bm',self.search_bookmarks)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        return {'commands':['bm:tag - searches bm.doomicile'],'additional':[]}

    def search_bookmarks(self, term):
        '''
        searches bm.doomicile.de for tagged entries
        '''
        result = ''
        term = term.strip()
        if term == '':
            return "Please specify your search term"

        bm = db.select(name="bm", udf=udfs.unnest_value, url="http://bm.doomicile.de/rss/all/"+quote_plus(term))

        result = 'Searching bookmarks for "%s"\n' % term
        if bm.rows:
            for row in bm.rows[0:5]:
                desc = row["bm$description"]+"\n" if len(row["bm$description"]) > 0 else ''
                result += '* %s' % row["bm$title"]
                if desc != '':
                    result += ': %s' % desc
                result += ' %s\n' % row["bm$link"]
        else:
            result += 'No sites found!'
        return self.strip_tags(result)



if __name__ == "__main__":
    import sys
    print Doomicile().search_bookmarks(sys.argv[1])
