from setuptools import setup
from pyviewx import __version__ as version
import os.path

descr_file = os.path.join( os.path.dirname( __file__ ), 'Readme.rst' )

setup( 
    name = 'PyViewX',
    version = version,

    packages = ['pyviewx', 'pyviewx.pygamesupport'],

    description = 'A library for communicating with eye trackers via the iViewX server software from SensoMotoric Instruments.',
    long_description = open( descr_file ).read(),
    author = 'Ryan Hope',
    author_email = 'rmh3093@gmail.com',
    url = 'https://github.com/RyanHope/PyViewX',
    classifiers = [
				'License :: OSI Approved :: GNU General Public License 3 (GPL-3)',
				'Programming Language :: Python :: 2',
				'Topic :: Utilities',
    ],
	license = 'GPL-3',
	install_requires = [
					'setuptools',
					'panglery',
					'twisted'
	],
 )
