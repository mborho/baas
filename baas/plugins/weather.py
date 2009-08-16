# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import urllib2
import urllib
import re
import chardet
from urllib import quote_plus
from xml.dom import minidom
from xml.etree import ElementTree
from baas.core.plugins import Plugin

try:
    # appengine
    from django.utils import simplejson
except:
    import simplejson

class Weather(Plugin):

    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('weather',self.forecast)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        additional = ''''''

        return {'commands':['weather:city [,country] [#lang] - get weather information and forecast'],'additional':[additional]}

    def _fix_invalid_xml(self, xml):
        #0xA0 0x25 0x22 0x2F
        encoding = chardet.detect(xml)['encoding']
        xml = xml.decode(encoding).encode('utf-8')            
        return xml

    def _sanitize(self, string):
        return string.encode('utf-8','ignore')

    def _api_request(self, location, lang):
        """
            makes a api-request and parses result
        """
        result = {'info':{}, 'current':{},'forecast':[]}
        #lang='en'
        try:
            url_term = urllib.urlencode({'weather':location.encode('utf-8').lower(),'hl':lang})
            
            api_url = 'http://www.google.de/ig/api?%s' % (url_term)

            req = urllib2.Request(api_url)
            response = urllib2.urlopen(req).read()
            if response:
                response = self._fix_invalid_xml(response)
                weather = ElementTree.fromstring(response)

                for e in weather.find('weather/forecast_information').getchildren():
                    result['info'][e.tag] = e.attrib.get('data').encode('utf-8','ignore')

                for e in weather.find('weather/current_conditions').getchildren():
                    result['current'][e.tag] = e.attrib.get('data').encode('utf-8','ignore')

                match = 'weather/forecast_conditions'
                forecasts = [e.getchildren() for e in weather.findall(match)]
                for fcast in forecasts:
                    day = {}
                    for e in fcast:
                        day[e.tag] = e.attrib.get('data').encode('utf-8','ignore')
                    result['forecast'].append(day)
        except:
            raise EnvironmentError, 'Forecast failed'
        return result

    def forecast(self, term):
        '''
        requests a weather forecast via google weather api 
        '''
        result = ''
        lang = 'en'
        if term == '':
            return "Please specify your location"

        pat = re.compile('(?P<term>[^#]*)\ ?(?P<lang>#[^\ @]*)?', re.I)
        cmds = pat.search(term)
        if cmds:
            term = cmds.group('term')
            lang = cmds.group('lang') or lang

        lang = lang.strip('#')
        term = term.strip()

        result = self._api_request(term, lang)
        return self.render(data=result, title=None)

    def render_xmpp(self, data, title):
        '''
        renders the result for xmpp responses
        '''
        i = data.get('info')
        result = '%s:\n' % (i.get('city'))#, i.get('current_date_time'))
        c = data.get('current')
        if c.get('condition'): 
            result += '%s, ' % c.get('condition')
        result += '%s°C/%s°F,' % (c.get('temp_c'), c.get('temp_f'))
        result += '%s\n%s\n\n' % (c.get('humidity'), c.get('wind_condition'))
        f = data.get('forecast')
        for d in f:
            result += '%s: ' % (d['day_of_week'])
            result += '%s (%s°/%s°)\n' % (d['condition'], d['low'], d['high'])
        return self.strip_tags(result.decode('utf-8'))

    def render_wave(self, data, title):
        '''
        renders the result for wave responses
        '''
        i = data.get('info')
        if i:
            result = " <br/><br/>"
            result += '<b>%s</b>:<br/><br/>' % (self.htmlentities_decode(i.get('city')))#, i.get('current_date_time'))
            c = data.get('current')
            if c.get('condition'): 
                result += '%s, ' % self.htmlentities_decode(c.get('condition'))
            result += '%s°C/%s°F, %s<br/>%s<br/><br/>' % (
                    c.get('temp_c'),
                    c.get('temp_f'),
                    self.htmlentities_decode(c.get('humidity')), 
                    self.htmlentities_decode(c.get('wind_condition'))
                    )
            f = data.get('forecast')
            for day in f:
                #icon = '<img src="http://google.com%s" alt="" />' % day['icon']
                result += '%s: %s (%s°/%s°)<br/>' % (
                    self.htmlentities_decode(day['day_of_week']),
                    self.htmlentities_decode(day['condition']), 
                    day['low'], 
                    day['high']
                    )        
        else:
            result = 'Request failed'
        return result.decode('utf-8')

