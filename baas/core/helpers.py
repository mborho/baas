# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import re
from htmlentitydefs import name2codepoint as n2cp
from datetime import datetime

xml_escapes = {
    '&' : '&amp;',
    '>' : '&gt;',
    '<' : '&lt;',
    #'"' : '&#34;',
    #"'" : '&#39;'
}

def xmlify(string):
    """
        makes a string xml valid
    """
    return re.sub(r'([&<>])', lambda m: xml_escapes[m.group()], strip_tags(string))

def strip_tags(value):
    """
        Return the given HTML with all tags stripped.
    """
    return re.sub(r'<[^>]*?>', '', value)        
    
def format_pub_date(date, fmt):
    dt = datetime.strptime(date,'%a, %d %b %Y %H:%M:%S +0000')
    return dt.strftime(fmt)
    

def substitute_entity(match):
    ent = match.group(3)

    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def htmlentities_decode(string):
    """ thanks to http://snippets.dzone.com/posts/show/4569 """
    entity_re = re.compile(r'&(#?)(x?)(\d{1,5}|\w{1,8});')
    return entity_re.subn(substitute_entity, string)[0]