---
layout: default
title: Python3
parent: Installation
nav_order: 1
---
1. TOC
{:toc}

## Python3 

In order to run OSAT you need to install **Python3**

You can find and download Python [here](https://www.python.org/downloads/)

## MacOS

### Is Python 3 already installed?
Before we start, make sure Python 3 isn’t already installed on your computer. Open up the command line via the Terminal application which is located at `Applications -> Utilities -> Terminal`.

Then type the command `python --version` followed by the Enter key to see the currently installed version of Python.

```Bash
$ python --version
Python 2.7.17
```

It’s possible that Python 3 may have already been installed as python3. Run the command `python3 --version` to check, however most likely this will throw an error.

### Install XCode
The first step for Python 3 is to install Apple’s Xcode program which is necessary for iOS development as well as most programming tasks. We will use XCode to install Homebrew.

In your Terminal app, run the following command to install XCode and its command-line tools:

```Bash
$ xcode-select --install
```
It is a large program so this make take a while to download. Make sure to click through all the confirmation prompts XCode requires.

### Install Homebrew
Next install Homebrew by copy/pasting the following command into Terminal and then type Enter:

```Bash
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
To confirm Homebrew installed correctly, run this command:

```Bash
$ brew doctor
```
Your system is ready to brew.

### Install Python 3
Now we can install the latest version of Python 3. Type the following command into Terminal and press Enter:

```Bash
$ brew install python3
```
To confirm which version of Python 3 was installed, run the following command in Terminal:

```Bash
$ python3 --version
Python 3.7.7
```
Finally, to run our new version of Python 3 open an interactive shall by typing python3 within Terminal:

```Bash
$ python3
Python 3.7.7 (default, Mar 10 2020, 02:16:23)
[Clang 11.0.0 (clang-1100.0.33.17)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
To exit the Python 3 interactive shell, you can type either exit() and then Return or type Control+d which means hold both the Control and D keys at the same time.