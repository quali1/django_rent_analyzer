from setuptools import setup, find_packages

setup(
    name='real-estate-analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'fake-useragent'
    ],
)