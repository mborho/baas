# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import urlencode, quote_plus
from baas.core.plugins import Plugin
from baas.core.helpers import strip_tags, xmlify, htmlentities_decode, load_url

try:
    # appengine
    from django.utils import simplejson
except:
    import simplejson

class Maemo (Plugin):

    def __init__(self, config, format='xmpp'):
        super(Maemo,self).__init__(config, format)
        self.result_limit = 8
        
    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('maemo',self.search)]
        return cmd_map

    def get_limits(self):
        """
            returns the limit map for the plugin commands
            for e.g. several result pages
        """
        limit_map = [('maemo',self.result_limit)]
        return limit_map
        
    def get_help(self):
        """
            returns the help text for the plugin
        """
        return {
            'commands': ['maemo:word [#talk, #packages or #wiki] - maemo.org search'],
            'additional': [''],
        }

    def _api_request(self, mode, params):
            
        url_params = urlencode( params )
        api_url = 'http://ajax.googleapis.com/ajax/services/search/'+mode+'?%s' % (url_params)

        response = load_url(api_url)
        api_response  = simplejson.loads(response)
        if api_response.get('responseStatus') == 200:
            return api_response
        else:
            return None

    def _extract_hits(self, result):
        if result:
            hits = result.get('responseData',{}).get('results')
            # handle single result
            if type(hits) == dict:
                hits = [hits]
            return hits
        else:
            return None

    def _build_query_term(self, term):
        return 'intitle:' + ' intitle:'.join(term.split())+' '

    def search(self, term):
        '''
        searches metacritic
        '''
        term = term.strip()
        what = 'talk'

        if term:
            (term, page) = self.extract_page_param(term)                            
            if term.find('#')+1:
                term, what = term.split('#',1)
                term = term.strip()
                
        if what == 'wiki':
            query = 'site:wiki.maemo.org %s' % (term)
            title = 'Wiki entries about %s\n' % term
        elif what == 'packages':
            query = 'site:maemo.org inurl:/packages/view/ %s' % (self._build_query_term(term))
            title = 'Packages for %s\n' % term
        else:
            query = 'site:talk.maemo.org inurl:showthread.php %s' % (term)
            title = 'Postings about %s\n' % term
        
        params = {
                'v':'1.0', 
                'q':query.encode('utf-8').lower(),
                'rsz':'large',
                'start':(page-1)*self.result_limit
                }
       
        response = self._api_request('web', params)
        hits = self._extract_hits(response)

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
