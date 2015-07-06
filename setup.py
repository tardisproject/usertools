import tardis

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='tardis-scriptkit',
    version=tardis.__version__,
    author=tardis.__author__,
    author_email=tardis.__authoremail__,
    description='Scriptkit for Tardis',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tardis = tardis.interactive:main',
        ]
    }
)
