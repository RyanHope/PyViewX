from setuptools import setup, find_packages
import os.path

__version__ = '0.5.1'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='pyviewx.pygame',
    version=__version__,
    
    namespace_packages=['pyviewx'],
    packages=['pyviewx.pygame'],

    description='A pygame calibration scene for use with PyViewX',
    long_description=open(descr_file).read(),
    author='Ryan Hope',
    author_email='rmh3093@gmail.com',
    url='https://github.com/RyanHope/PyViewX',
    classifiers=[
				'License :: OSI Approved :: GNU General Public License (GPL)',
				'Framework :: Twisted',
				'Programming Language :: Python :: 2',
				'Topic :: Scientific/Engineering',
				'Topic :: Utilities',
                'Topic :: Software Development :: Libraries :: pygame'
    ],
	license='GPL-3',
	install_requires=[
					'panglery',
					'twisted',
                    'pygame',
                    'pyviewx.client >= 0.5.0'
	],
 )
