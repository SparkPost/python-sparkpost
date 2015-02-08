from codecs import open
from setuptools import setup

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='sparkpost',
    version='1.0.0.dev1',
    author='Message Systems',
    author_email='appteam@messagesystems.com',
    packages=['sparkpost'],
    url='https://github.com/SparkPost/python-sparkpost',
    license='Apache 2.0',
    description='SparkPost Python API client',
    long_description=readme,
    install_requires=['requests==2.5.1'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
