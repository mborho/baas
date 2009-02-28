# -*- coding: utf-8 -*-
from baas.core.plugins import Plugin

class Help(Plugin):

    def man(self, cmd=None):
        result = ''
        if cmd == 'list':
            result = '''Available commands:
bm:tag - searches bm.doomicile
news:word - searches for news
web:word - websearch

Some commands (news,web) can be combined with #de, examples:
news:hamburg #de
web:xmpp #de

cheers!
            '''
        return result



if __name__ == "__main__":
    import sys
    print Help().man(sys.argv[1])
