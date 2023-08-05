from setuptools import find_packages, setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

long_description = 'Import get_n_top_colors command to work with'

setup(
    name='top_color_pct',
    packages=find_packages(),
    version='0.1.0',
    description='This library allows you to take N top colors from the image',
    author='NasciNSC',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='MIT',
    install_requires=['webcolors'],
    keywords=['python', 'image', 'processing', 'img', 'top_colors', 'color', 'analitics'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)