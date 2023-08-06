from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'A Package for interacting with Discord\'s API'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="gydo.py",
    version=VERSION,
    author="loldonut (John Heinrich)",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=['requests', 'schedule', 'websockets', 'aiohttp', 'next_asyncio', 'pymitter'],
    keywords=['python', 'discord', 'gydo.py', 'discord api']
)