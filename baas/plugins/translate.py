# -*- coding: utf-8 -*-
import re
import urllib2
from urllib import quote_plus
import simplejson
from baas.core.plugins import Plugin

class Translate(Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('tlate',self.translate)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        additional = '''
A translation needs the target language specified by a hashtag
tlate:Wie gehts?  #en
tlate:Wie gehts?  #es
tlate:How do you do? #de'''

        return {'commands':['tlate:word #en - translates the word in german in english, #LANG sepcifies the target lang'],'additional':[additional]}

    def _api_request(self, term, target_lang):
        result = ''
        detected_lang = None
        try:
            url_term = quote_plus(term.encode('utf-8').lower())
            api_url = 'http://www.google.com/uds/Gtranslate?context=22&q=%s&langpair=|%s&key=notsupplied&v=1.0' % (url_term, target_lang)

            req = urllib2.Request(api_url)
            response = urllib2.urlopen(req).read()
            api_response  = simplejson.loads(response)
            if api_response.get('responseStatus') == 200:
                translate_data = api_response.get('responseData')
                detected_lang = translate_data.get('detectedSourceLanguage')
                result = translate_data.get('translatedText')
        except:
            raise EnvironmentError, 'Translation failed'
        return result, detected_lang

    def translate(self, term):
        '''
        example plugin
        '''
        result = ''
        lang = 'de'       
        if term == '':
            return "Please specify your text to translate"

        if term and term.find('#')+1:
            term, lang = term.split('#',1)
            term = term.strip()

        translated_text, detected_lang = self._api_request(term, lang)
        if translated_text:
            result = '%s (%s => %s)' % (translated_text, detected_lang, lang)
        else:
            result = 'Text translation failed'

        return self.strip_tags(result)

