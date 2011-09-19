#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

# Process the includes, excludes and packages first

includes = []
excludes = []
packages = ['re']
path = []

# This is a place where the user custom code may go. You can do almost
# whatever you want, even modify the data_files, includes and friends
# here as long as they have the same variable name that the setup call
# below is expecting.

# No custom code added

# use the Python class Executable from cx_Freeze


GUI2Exe_Target_1 = Executable(
    # what to build
    script = "PomodoroTk.py",
    initScript = None,
    #base = 'Win32GUI',
    #targetDir = r"dist",
    #targetName = "PomodoroTk",
    compress = False,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = None)


# That's serious now: we have all (or almost all) the options cx_Freeze
# supports. I put them all even if some of them are usually defaulted
# and not used. Some of them I didn't even know about.

setup(

    version = "0.4",
    description = "A simple Pomodoro Timer written with Python 3 and Tkinter.",
    author = "Felix Lu",
    name = "PomodoroTk",

    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path}},

    executables = [GUI2Exe_Target_1])

# This is a place where any post-compile code may go.
