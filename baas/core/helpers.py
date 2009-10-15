# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import re
from datetime import datetime

def strip_tags(value):
    """
        Return the given HTML with all tags stripped.
    """
    return re.sub(r'<[^>]*?>', '', value)        

def xmlify(string):
    """
        makes a string xml valid
    """
    return re.sub(r'([&<>])', lambda m: xml_escapes[m.group()], strip_tags(string))
    
def format_pub_date(date, fmt):
    dt = datetime.strptime(date,'%a, %d %b %Y %H:%M:%S +0000')
    return dt.strftime(fmt)
    
