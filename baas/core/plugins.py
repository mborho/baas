#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import new
from baas import plugins

class PluginLoader(object):

    def __init__(self):
        self.plugins = {}
        self.help = ''
        self.commands = {}

    def load_plugins(self):
        for file in os.listdir(plugins.__path__[0]):
            file_parts = os.path.splitext(file)
            if  file_parts[1] == '.py' and file[0:2] != '__':
                self.plugins[file_parts[0].capitalize()] = getattr(__import__('baas.plugins.'+file_parts[0], globals(), locals(),[file_parts[0].capitalize()]),file_parts[0].capitalize())()

    def load_map(self):
        for name in self.plugins:
            cmd_map = self.plugins[name].get_map()
            if cmd_map:
                for (cmd,func) in cmd_map:
                    self.commands[cmd] = func

    def load_help(self):
        help_infos = {}
        help_list = []
        help_additional = []
        for name in self.plugins:
            help_info = self.plugins[name].get_help()
            if help_info:
                help_infos[name] = help_info

        for h in help_infos:
            for t in help_infos[h].get('commands'):
                help_list.append(t)
            for a in help_infos[h].get('additional'):
                help_additional.append(a)

        self.help = "\n".join(help_list)
        self.help += "\n%s" % "\n".join(help_additional)           

class Plugin(object):

    def __init__(self):
        pass

    def get_map(self):
        return None

    def get_help(self):
        return None

    def test(self):
        print "test"
            #if os.path.fileext(file) == "py": print "kjhK"
        #className = className.capitalize()
        #try:
            ##pluginClass = __import__(__name__, None, None,['Importer.plugins'])
            ##aClass = pluginClass.__getattribute__(className)
            #aClass = getattr(__import__(__name__,globals(),locals(),['Importer.plugins']),className)
            #return apply(aClass, args)
        #except:
            #return None

    def strip_tags(self, value):
        """
            Return the given HTML with all tags stripped.
        """
        return re.sub(r'<[^>]*?>', '', value)        

