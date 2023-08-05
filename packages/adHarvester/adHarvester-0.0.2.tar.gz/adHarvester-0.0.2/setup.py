from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Web site harvester which takes input as json required fields and return all info related to input fields'
LONG_DESCRIPTION = 'Web site harvester which takes input as json required fields and return all info related to input fields'

setup(
    name="adHarvester",
    version=VERSION,
    author="Suren Abrahamyan",
    author_email="suren.abrahamyan89@gmail.com",
    description='Harvester for any type of online shops and advertisements',
    long_description='Harvester for any type of online shops and advertisements',
    packages=find_packages(),
    license='MIT',
    url = 'https://github.com/surenab/adHarvester',
    download_url = 'https://github.com/surenab/adHarvester/archive/refs/tags/0.0.2.tar.gz',
    keywords=['python', 'harvester', 'scraper', 'extract', 'soup', 'requests'],
    install_requires=[
        'js2py',
        'bs4',
        'requests',
        'lxml',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)