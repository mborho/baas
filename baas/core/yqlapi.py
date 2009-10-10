#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import urllib
import urllib2

try:
    # appengine
    from django.utils import simplejson
except:
    import simplejson

class YQLApi(object):
    def __init__(self, app_key=None, logger=None):
        self.app_key = app_key
        self.logger = logger
        
    def log(self, msg):
        if self.logger:
            self.logger.info(msg)
        
    def request(self, type_, query, **kwargs):

        self.log('Query:%s'%query)
        self.log('type_:%s'%type_)
        self.log('Other Args:%s'%kwargs)

        base_url = 'http://query.yahooapis.com/v1/public/yql?q=%s&format=json'
        base_url += '&diagnostics=false&callback='
        yql_query = urllib.quote_plus(query.encode('utf-8'))
        final_url = base_url % (yql_query)
        self.log('final_url: %s'%final_url)

        response=urllib.urlopen(final_url)
        api_data=simplejson.load(response)
        result = api_data.get('query',{}).get('results',{})

        hits = result.get('result') if result else None
        
        # handle single result
        if type(hits) == dict:
            hits = [hits]

        self.log('data:%s'% hits)        
        return hits
        
    def web(self, query, **kwargs):                    
        return self.request('web', query, **kwargs)
       
    def news(self, query, **kwargs):
       return self.request('news', query, **kwargs)
