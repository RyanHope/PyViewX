from distutils.core import setup
from panglery import __version__ as version
import os.path

descr_file = os.path.join( os.path.dirname( __file__ ), 'README.rst' )

setup( 
    name = 'PyViewX',
    version = version,

    packages = ['PyViewX'],

    description = 'A library for communicating with eye trackers via the iViewX server software from SensoMotoric Instruments.',
    long_description = open( descr_file ).read(),
    author = 'Ryan Hope',
    author_email = 'rmh3093@gmail.com',
    url = 'https://github.com/RyanHope/PyViewX',
    classifiers = [
        'License :: OSI Approved :: GPL 3',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
 )
