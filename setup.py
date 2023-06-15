from distutils.core import setup

description = '''
This is some dope code for GW Instek GPD-x303S power supplies.
'''

setup(name='gpdx303s',
      version='1.1.0',
      description='Python Interface for GW Instek GPD-x303S power supplies',
      author='Tom Pickard',
      author_email='tom@pickard.dev',
      license='BSD License',
      platforms=['Linux'],
      url='https://github.com/nailshard/gpdx303s',
      py_modules=['gpdx303s'],
      install_requires=['pyserial'],
      classifiers=['Topic :: Terminals :: Serial',
                   'Development Status :: 5 - Production/Stable',
                   'Programming Language :: Python',
                   ],
      long_description=description
      )
