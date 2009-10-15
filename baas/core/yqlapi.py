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
    def __init__(self, community=None, app_key=None, logger=None):
        self.app_key = app_key
        self.logger = logger
        self.community = community
        
    def log(self, msg):
        if self.logger:
            self.logger.info(msg)
        
    def request(self, query, **kwargs):

        base_url = 'http://query.yahooapis.com/v1/public/yql?q=%s&format=json'
        base_url += '&diagnostics=false&callback='
        community_param = None
        if self.community:            
            community_param= '&env='+urllib.quote_plus('store://datatables.org/alltableswithkeys')
            
        yql_query = urllib.quote_plus(query.encode('utf-8'))
        final_url = base_url % (yql_query)
        
        if self.community:            
            final_url += '&env='+urllib.quote_plus('store://datatables.org/alltableswithkeys')
        
        response=urllib.urlopen(final_url)
        api_data=simplejson.load(response)
        result = api_data.get('query',{}).get('results',{})

        return result
