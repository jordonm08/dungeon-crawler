"""
Setup script for building Dungeon Crawler macOS app
"""
from setuptools import setup

APP = ['dungeon_crawler.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['pygame'],
    'plist': {
        'CFBundleName': 'Dungeon Crawler',
        'CFBundleDisplayName': 'Dungeon Crawler',
        'CFBundleIdentifier': 'com.jordonmyers.dungeoncrawler',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    }
}

setup(
    name='Dungeon Crawler',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
