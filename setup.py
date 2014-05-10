#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PomodoroTk",
        version = "0.7",
        description = "A simple Pomodoro Timer written with Python 3 and Tkinter.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("PomodoroTk.py", base=base, icon='PomodoroTk.ico')])
