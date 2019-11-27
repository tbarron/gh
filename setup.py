"""
This is free and unencumbered software released into the public domain.
For more details, please visit <http://unlicense.org/>.
"""
from gh import version
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="gh",
    version=version._v,
    description="Github project manager",
    author="Tom Barron",
    author_email="tusculum@gmail.com",
    packages=['gh'],
    entry_points = {
        'console_scripts': ['gh=gh.__main__:main']
    },
    data_files=[
        ('pkg_data/gh/info', [
                              './LICENSE',
                              './README.md',
                              'CHANGELOG.md',
                              ]),
    ],
    url="... update this ...",
    download_url="... update this ...",
    )
