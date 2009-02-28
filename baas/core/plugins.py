#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class Plugin(object):

    def __init__(self):
        pass
        

    def strip_tags(self, value):
        """
            Return the given HTML with all tags stripped.
        """
        return re.sub(r'<[^>]*?>', '', value)        
