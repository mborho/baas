# -*- coding: utf-8 -*-
# Copyright 2010 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from urllib import quote_plus
from baas.core.yqlapi import YQLApi
from baas.core.plugins import Plugin
from baas.core.helpers import strip_tags, xmlify, htmlentities_decode

class Music (Plugin):

    def __init__(self, config, format='xmpp'):
        super(Music,self).__init__(config, format)
        self.result_limit = 10
        
    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('music',self.search)]
        return cmd_map

    def get_limits(self):
        """
            returns the limit map for the plugin commands
        """
        limit_map = [('music',self.result_limit)]            
        return limit_map
        
    def get_help(self):
        """
            returns the help text for the plugin
        """
        additional = '''music:stooges #artist (default)
music:funhouse #release
music:dog #track'''

        return {
            'commands': ['music:name [#artist,#release or #track] - searches for artists,release or track'],
            'additional': [additional],
        }

    def _get_offset(self, page):
        return (page-1)*self.result_limit
        
    def _get_artist(self, row):
        artist = row.get('Artist',{})
        if isinstance(artist, list): artist = artist[0]
        return artist

    def _extract_hits(self, result, name):
        hits = result.get(name) if result else None    
        # handle single result
        if type(hits) == dict:
            hits = [hits]
        return hits
        
    def search(self, term):
        '''
        searches web by yahoo
        '''
        term = term.strip()
        what = 'artist'
        page = 1
        if term:
            (term, page) = self.extract_page_param(term)                            
            if term.find('#')+1:
                term, what = term.split('#',1)
                term = term.strip()

        if term == '':
            return "Please specify your search term"

        # handle single and double quotes
        term = term.replace("'",'"')

        query = 'select * '
        query += 'from music.%s.search(%d,%d) where keyword=\'%s\' ' % (what, self._get_offset(page), self.result_limit, term)

        yql_api = YQLApi()
        response = yql_api.request(query=query)
        title = 'Searching %ss for %s\n' % (what, term)
        return self.render(data=response, title=title)

    def render_xmpp(self, response, title):
        '''
        renders the result for xmpp responses
        '''
        result = title+"\n"
        if response:
            if response.get('Artist'):
                artists = self._extract_hits(response, 'Artist')
                for row in artists:
                    result += "%s : %s\n" % (row.get('name'), row.get('url'))
            elif  response.get('Release'):
                releases = self._extract_hits(response, 'Release')
                for row in releases:
                    artist = self._get_artist(row)
                    result += '"%s" (%s) by %s : %s\n' % (row.get('title'), row.get('releaseYear'), artist.get('name'), row.get('url'))
            elif  response.get('Track'):
                tracks = self._extract_hits(response, 'Track')
                for row in tracks:
                    artist = self._get_artist(row)
                    result += '"%s" (%s) by %s : %s\n' % (row.get('title'), row.get('releaseYear'), artist.get('name'), row.get('url'))
        else:
            result += 'No hits found!'
        
        return strip_tags(result)

    def render_wave(self, response, title):
        '''
        renders the result for wave responses
        '''
        result = " <br/><br/><b>%s</b><br/>" % xmlify(title)
        if response:
            if response.get('Artist'):
                artists = response.get('Artist')
                for row in artists:
                    title = xmlify(row['name'])
                    result += '<a href="%s">%s</a><br/><br/>' % (xmlify(row['name']), title)
            elif  response.get('Release'):
                releases = self._extract_hits(response, 'Release')
                for row in releases:
                    artist = self._get_artist(row)
                    result += '<a href="%s">%s</a> (%s) by <a href="%s">%s</a><br/><br/>\n' % (xmlify(row.get('url')), xmlify(row.get('title')), \
                            xmlify(row.get('releaseYear')), xmlify(artist.get('url')), xmlify(artist.get('name')) )
            elif  response.get('Track'):
                tracks = self._extract_hits(response, 'Track')
                for row in tracks:
                    artist = self._get_artist(row)
                    result += '<a href="%s">%s</a> (%s) by <a href="%s">%s</a><br/><br/>\n' % (xmlify(row.get('url')), xmlify(row.get('title')), \
                            xmlify(row.get('releaseYear')), xmlify(artist.get('url')), xmlify(artist.get('name')) )
        else:
            result += 'No hits found!'
        return result
