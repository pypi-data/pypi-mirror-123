from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='lolpros_parser',
      packages = ['lolpros_parser'],
      version='0.0.3',
      description='Python Parser for lolpros.gg',
      url='http://github.com/samhine/lolpros_parser',
      download_url="https://github.com/samhine/lolpros_parser/archive/refs/tags/0.0.3.zip",
      author='Samuel Hine',
      author_email='sam.hine27@gmail.com',
      keywords=['PYTHON', 'LOLPROS', 'API'],
      license='MIT',
      install_requires=['requests'],
      long_description_content_type='text/markdown',
      long_description=long_description)