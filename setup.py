""" Schemabridge packaging instructions """

from setuptools import setup, find_packages

setup(
    name='schemabridge',
    packages=['schemabridge'],
    version='0.1',
    description='CLI interface for Schemaverse,'
    author='FrozenFOXX',
    author_email='frozenfoxx@churchoffoxx.net',
    url='https://github.com/frozenfoxx/schemabridge',
    download_url='https://github.com/frozenfoxx/schemabridge/archive/0.1.tar.gz',
    keywords=['schemaverse', 'postgresql', 'cli'],
    classifiers=[],
    install_requires=[
        'psycopg2'
    ],
    scripts=[
        'scripts/schemabridge',
    ],
    data_files=[
        ('/etc/schemabridge', ['conf/schemabridge.conf'])
    ],
)
