from setuptools import setup, find_packages
# from codecs import open
import io
from os import path

# --- get version ---
version = "unknown"
with open("rock_avatars/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', '')
# --- /get version ---


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rock_avatars',
    version=version,
    description='Rockflow Avatars generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/day253/rock-avatars',
    author='Junkai Dai',
    author_email='daijunkai@flowcapai.com',
    platforms=['any'],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=[
        'Pillow',
    ],
)