# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
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

        feed = self.load_feed(twingly_rss)

        if content == 'blog': limit = 5
        else: limit = 10

        title = '%s search for %s' % (content, term)
        hits = None
        if feed.entries:
            hits = feed.entries[0:limit]

        return self.render(data=hits, title=title, extra_format=content)

        if feed.entries:            
            for row in feed.entries[0:limit]:
                desc = row["summary"]+"\n" if len(row["summary"]) > 0 else ''
                result += '* %s' % row["title"]
                if desc != '' and content== 'blog':
                    result += ': %s' % desc
                result += '%s\n' % row["link"]
            result = self.htmlentities_decode(result)
        else:
            result += 'No sites found!'

        return result

    def blogs(self, term):
        '''
        blog search
        '''
        result = self._search(term, 'blog')
        return result


    def microblogs(self, term):
        '''
        microblog search
        '''
        result = self._search(term, 'microblog')
        return result

    def render_xmpp_blog(self, data, title):
        '''
        renders the blog result for xmpp responses
        '''
        result = title+"\n"
        if data:
            for row in data:
                desc = row["summary"]+"\n" if len(row["summary"]) > 0 else ''
                result += '* %s' % row["title"]
                if desc != '':
                    result += ': %s' % desc
                result += '%s\n' % row["link"]
            result = self.htmlentities_decode(result)
        else:
            result += 'No sites found!'
        return self.strip_tags(result)

    def render_wave_blog(self, data, title):
        '''
        renders the blog result for wave responses
        '''
        result = " <br/><br/><b>%s</b><br/>" % self.xmlify(title)
        if data:
            for row in data:
                result += '<a href="%s">%s</a><br/>' % (self.xmlify(row["link"]), self.xmlify(row["title"]))
                desc = row["summary"] if len(row["summary"]) > 0 else None
                if desc:
                    result += "%s<br/>" % self.xmlify(self.htmlentities_decode(desc))
                result += '<br/>'
        else:
            result += 'No sites found!'
        return result

    def render_xmpp_microblog(self, data, title):
        '''
        renders the microblog result for xmpp responses
        '''
        result = title+"\n"
        if data:
            for row in data:
                desc = row["summary"]+"\n" if len(row["summary"]) > 0 else ''
                result += '* %s' % row["title"]
                if desc != '':
                    result += ': %s' % desc
                result += '%s\n' % row["link"]
            result = self.htmlentities_decode(result)
        else:
            result += 'No sites found!'
        return self.strip_tags(result)

    def render_wave_microblog(self, data, title):
        '''
        renders the microblog result for wave responses
        '''
        result = " <br/><br/><b>%s</b><br/>" % self.xmlify(title)
        if data:
            for row in data:
                result += '%s <a href="%s">link</a><br/><br/>' % (self.xmlify(row["title"]), self.xmlify(row["link"]))
        else:
            result += 'No sites found!'
        return result 
