from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.0.0'
tests_require = [
    'mock',
    'webtest',
    'pytest',
]

setup(
    name='msg_router',
    version=version,
    packages=find_packages(),
    install_requires=[
        'pyramid>=1.5,<1.6'
        'netaddr>=0.7,<0.8'
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
)
