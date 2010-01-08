# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import urlencode, quote_plus
import urllib2
from baas.core.plugins import Plugin
from baas.core.helpers import strip_tags, xmlify, htmlentities_decode

try:
    # appengine
    from django.utils import simplejson
except:
    import simplejson

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

    def _api_request(self, mode, params):
            
        api_url = 'http://ajax.googleapis.com/ajax/services/search/'+mode+'?%s' % (params)
        
        req = urllib2.Request(api_url)
        response = urllib2.urlopen(req).read()
        api_response  = simplejson.loads(response)
        if api_response.get('responseStatus') == 200:
            return api_response
        else:
            return None

    def _extract_hits(self, result):
        hits = result.get('responseData',{}).get('results')
        # handle single result
        if type(hits) == dict:
            hits = [hits]
        return hits
         
    def web(self, term):
        '''
        searches web by yahoo
        '''
        term = term.strip()
        lang = 'en'

        if term and term.find('#')+1:
            term, lang = term.split('#',1)
            term = term.strip()

        params = urlencode( {
                'v':'1.0', 
                'q':term.encode('utf-8').lower(),
                'hl':lang, 
                'gl':lang,
                'rsz':'large',
                }
        )
        response = self._api_request('web', params)
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

        params = urlencode( {
                'v':'1.0', 
                'q':term.encode('utf-8').lower(),
                'ned':lang, 
                'rsz':'large',
                #'scoring':'d',
                }
        )
        response = self._api_request('news', params)
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
                result += "%s - %s\n" % (htmlentities_decode(title), row['unescapedUrl'])
        else:
            result += 'No hits found!'
        return strip_tags(result)

    def render_wave(self, hits, title):
        '''
        renders the result for wave responses
        '''
        result = " <br/><br/><b>%s</b><br/>" % xmlify(title)
        if hits:
            for row in hits:
                title = row['titleNoFormatting']
                if row.get('publisher'):
                    title = "%s: %s" % (row.get('publisher'), title)
                title = xmlify(htmlentities_decode(title))
                result += '<a href="%s">%s</a><br/><br/>' % (xmlify(row['unescapedUrl']), title)
        else:
            result += 'No hits found!'
        return result
