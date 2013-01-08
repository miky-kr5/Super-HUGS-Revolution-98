Super HUGS Revolution 98
========================

A simple python game for Android by Miguel Angel Astor.

License
-------

Super HUGS Revolution 98 for Android is available under the
terms of a FreeBSD style license. See the file "COPYING" for
details of the license.

Description
-----------

In Super HUGS Revolution you are Moncho, a jolly guy who loves
people so much he likes to hug them until they explode!

System Requirements
-------------------

Super HUGS Revolution should run without problems on any system
compatible with Python 2.7 and Pygame. Running on Android
requires a minimum of Android 2.2 (API 8).

Compilation for Android
-----------------------

Super HUGS Revolution 98 depends on Python 2.7, Pygame 1.9.1, pgs4a 0.9.4.

To compile Super HUGS Revolution for Android devices you need a
working installation of Pygame Subset for Android (pgs4a) by
Tom Rothamel and Patrick Dawson. pgs4a can be
found at the following link:

    http://pygame.renpy.org/

Follow this steps to compile the game (instrucctions for GNU/Linux systems):

    1) Move the Super-HUGS-Revolution-98 directory inside the pgs4a directory.
    2) Cd to the pgs4a directory.
    3) Execute "./android.py configure Super-HUGS-Revolution-98".
    4) Answer the questions that will appear on the terminal.
    5) Execute "./android.py build Super-HUGS-Revolution-98 release".

This will produce a installable .apk file inside the bin directory of pgs4a.
Compiling on Windows systems is similar.

Installation
------------

To install Super HUGS Revolution on an Android device, use adb:

    adb install Super-HUGS-Revolution-98-X.Y.apk

You can also compile and install with the following command:

    ./android.py build Super-HUGS-Revolution-98 release

To play on a PC just execute the main.py script of Super HUGS Revolution 98.

How to play
-----------

Coming soon.
