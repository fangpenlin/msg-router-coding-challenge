from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.0.0'
try:
    import msg_router
    version = msg_router.__version__
except ImportError:
    pass

tests_require = [
    'mock',
    'webtest',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
]

setup(
    name='msg_router',
    version=version,
    packages=find_packages(),
    install_requires=[
        'pyramid>=1.5,<1.6',
        'netaddr>=0.7,<0.8',
        'jsonschema>=2.4,<2.5',
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
    entry_points="""\
    [paste.app_factory]
    main = msg_router:main
    """
)
