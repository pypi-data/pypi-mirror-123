from setuptools import setup

setup(name='tag2bio',
    version='0.4',
    description='A package created for translating tag formatted text to BIO formatted text.',
    packages=['tag2bio'],
    install_requires=['beautifulsoup4==4.10.0'],
    zip_safe=False
)