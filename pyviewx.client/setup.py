from setuptools import setup
import os.path

__version__ = '0.5.1'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='pyviewx.client',
    version=__version__,
    
    namespace_packages=['pyviewx'],
    packages=['pyviewx.client'],

    description='A package for communicating with eye trackers via the iViewX server software from SensoMotoric Instruments.',
    long_description=open(descr_file).read(),
    author='Ryan Hope',
    author_email='rmh3093@gmail.com',
    url='https://github.com/RyanHope/PyViewX',
    classifiers=[
				'License :: OSI Approved :: GNU General Public License (GPL)',
				'Framework :: Twisted',
				'Programming Language :: Python :: 2',
				'Topic :: Scientific/Engineering',
				'Topic :: Utilities'
    ],
	license='GPL-3',
	install_requires=[
					'panglery',
					'twisted'
	],
 )
