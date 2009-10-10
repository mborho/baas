from setuptools import setup, find_packages
import sys, os

version = '0.1.4.1'

setup(name='baas',
      version=version,
      description="'Buddy as a Service' is a xmpp / wavelet robot using Yahoo YQL API, Google API and other services to do searches and some other stuff (translations, weather forecast, etc) for you.",
      long_description="""\
The XMPP bot also runs on the google appengine. BaaS is easy extensible through plugins.  No API Keys required! \
See http://mborho.github.com/baas for more infos.
""",
      classifiers=[
        "Programming Language :: Python :: 2.5",
        "Topic :: Communications :: Chat", 
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Other Audience",
        "Operating System :: POSIX :: Linux",
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='xmpp',
      author='Martin Borho',
      author_email='martin@borho.net',
      url='http://mborho.github.com/baas',
      license='GNU General Public License (GPL)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      #data_files=[('conf',"conf/baas.conf")],

      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'twisted',
        'feedparser',
        'chardet',
        'simplejson'
      ],
      entry_points="""
      [console_scripts]  
      baas_bot = baas.scripts.bot:main
      """,       
      )
