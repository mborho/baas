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

class BossApi(object):
    def __init__(self, app_key, logger=None):
        self.app_key = app_key
        self.logger = logger
        
    def log(self, msg):
        if self.logger:
            self.logger.info(msg)
        
    def request(self, type_, query, **kwargs):
        self.log('Query:%s'%query)
        self.log('type_:%s'%type_)
        self.log('Other Args:%s'%kwargs)

        base_url = 'http://boss.yahooapis.com/ysearch/%s/v1/%s?%s'
        kwargs['appid'] = self.app_key
        payload = urllib.urlencode(kwargs)
        final_url = base_url%(type_, urllib.quote_plus(query), payload)
        self.log('final_url: %s'%final_url)

        response=urllib.urlopen(final_url)
        api_data=simplejson.load(response)
        result = api_data.get('ysearchresponse')
        print result
        self.log('data:%s'% result)        
        return result
        
    def web(self, query, **kwargs):                    
        return self.request('web', query, **kwargs)
       
    def news(self, query, **kwargs):
       return self.request('news', query, **kwargs)
#        
#    def do_spelling_search(self, query, **kwargs):
#        return self.talk_to_yahoo('spelling', query, **kwargs)
#    
#    def do_images_search(self, query, **kwargs):
#        return self.talk_to_yahoo('images', query, **kwargs)
#    
#    def do_siteexplorer_search(self, query, **kwargs):
#        return self.talk_to_yahoo('se_inlink', query, **kwargs)
