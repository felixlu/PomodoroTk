"""
Script for building the Mac OS X app of PomodoroTk.

Usage:
    python3 setup.py py2app
"""
from setuptools import setup

APP = ['PomodoroTk.py']
DATA_FILES = []
OPTIONS = {
    'iconfile':'PomodoroTk.icns',
    'plist': {'CFBundleShortVersionString':'0.7.0',}
}

setup(
    app=APP,
    name='PomodoroTk',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
