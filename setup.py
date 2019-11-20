from gh import version
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description="Github project manager",
    author="Tom Barron",
    author_email="tusculum@gmail.com",
    url="... update this ...",
    download_url="... update this ...",
    version=version._v,
    name="gh",
    )
