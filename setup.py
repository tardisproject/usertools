import tardis

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='tardis-scriptkit',
    version=tardis.__version__,
    author=tardis.__author__,
    author_email=tardis.__authoremail__,
    description='Scriptkit for Tardis',
    packages=['tardis'],
    entry_points={
        'console_scripts': [
            'tardis = tardis.script:main',
        ]
    }
)
