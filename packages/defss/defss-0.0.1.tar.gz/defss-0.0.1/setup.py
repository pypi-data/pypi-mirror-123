from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'defss',
    version = '0.0.1',
    description = 'defs needed for IgBot',
    long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Oliver Gorgiev',
    author_email = 'ogorgiev1@gmail.com',
    licence = 'MIT',
    classifiers = classifiers,
    keywords = 'defs',
    packages = find_packages(),
    install_requires = ['']

)