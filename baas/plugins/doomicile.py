# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
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

        url="http://bm.doomicile.de/rss/all/"+quote_plus(term)
        feed = self.load_feed(url)
        title = 'Searching bookmarks for %s' % term
        return self.render(data=feed.entries, title=title)

    def render_xmpp(self, data, title):
        '''
        renders the result for xmpp responses
        '''
        result = title+"\n"
        if data:
            for row in data[0:5]:
                desc = row["summary"]+"\n" if len(row["summary"]) > 0 else ''
                result += '* %s' % row["title"]
                if desc != '':
                    result += ': %s' % desc
                result += ' %s\n' % row["link"]
        else:
            result += 'No sites found!'
        return self.strip_tags(result)

    def render_wave(self, data, title):
        '''
        renders the result for wave responses
        '''
        result = " <br/><div><b>%s</b></div>" % self.xmlify(title)
        if data:
            for row in data[0:5]:
                result += '<a href="%s">%s</a><br/>' % (self.xmlify(row["link"]), self.xmlify(row["title"]))
                desc = row["summary"] if len(row["summary"]) > 0 else None
                if desc:
                    result += "%s<br/>" % self.xmlify(desc)
        else:
            result += 'No sites found!'
        return result


if __name__ == "__main__":
    import sys
    print Doomicile().search_bookmarks(sys.argv[1])
