from distutils.core import setup

description = '''
Library for GW Instek GPD-x303S power supplies.
'''

setup(name='gpdx303s',
      version='2.0.0',
      description='Python Interface for GW Instek GPD-x303S power supplies',
      author='dflachsqi2',
      author_email='',
      license='MIT License',
      platforms=['Linux'],
      url='https://github.com/dflachsqi2/PyGPD3303S',
      py_modules=['gpdx303s'],
      install_requires=['pyserial'],
      classifiers=['Topic :: Terminals :: Serial',
                   'Development Status :: 5 - Production/Stable',
                   'Programming Language :: Python',
                   ],
      long_description=description
      )
