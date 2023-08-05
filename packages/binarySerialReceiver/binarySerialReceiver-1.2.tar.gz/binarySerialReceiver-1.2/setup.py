import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'binarySerialReceiver',
  packages = ['binarySerialReceiver'],
  version = '1.2',
  license='MIT',
  description = 'Simple module for receiving binary data from a serial port',
  author = 'Francisco Liebl',
  author_email = 'chicolliebl@gmail.com',
  url = 'https://github.com/ChicoLiebl/python-binarySerialReceiver.git',
  download_url = 'https://github.com/ChicoLiebl/python-binarySerialReceiver/archive/refs/tags/V1.2.tar.gz',
  keywords = ['SERIAL', 'PORT', 'RECEIVER', 'BINARY', 'THREADED', 'BACKGROUND'],
  install_requires=[
          'numpy',
          'pyserial',
      ],
  long_description=long_description,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Communications',
    'Topic :: Terminals :: Serial',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)