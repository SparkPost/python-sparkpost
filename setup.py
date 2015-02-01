import sparkpost

from distutils.core import setup

setup(
    name='sparkpost',
    version=sparkpost.__version__,
    author='Message Systems',
    author_email='appteam@messagesystems.com',
    packages=['sparkpost'],
    url='https://github.com/SparkPost/python-sparkpost',
    license='Apache 2.0',
    description='SparkPost Python API client',
    long_description=open('README.rst').read(),
    install_requires=['requests==2.5.1'],
    zip_safe=False,
)
