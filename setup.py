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

    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
)
