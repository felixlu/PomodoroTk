# 0. Introduction

PomodoroTK is a simple Pomodoro Timer written with Python 3 and its built-in GUI library Tkinter.

* Author: Felix Lu <lugh82@gmail.com>
* License: GNU GPL

# 1. Requirement

* Python3

# 2. Run

Just clone this repository and cd to this folder in Terminal, then run the following command:

    $ python3 PomodoroTK.py

# 3. Compile .py to executable

## 3.1 Windows/Linux


### 3.1.1 Requirement

* cx_Freeze

### 3.1.2 Compile

Run the following command in Terminal:

    $ python3 setup.py build

The compiled executable files will be placed in the "build" folder of the PomodoroTk.

## 3.2 Mac OSX

### 3.2.1 Requirement

* py2app

### 3.2.2 Compile

Run the following command in Terminal:

    $ python3 setup2app.py py2app
