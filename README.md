Super HUGS Revolution 98
========================

A simple python game for Android by Miguel Angel Astor.

Description
-----------

In Super HUGS Revolution you are Moncho, a jolly guy who loves
people so much he likes to hug them until they explode!

System Requirements
-------------------

Super HUGS Revolution should run without problems on any system
compatible with Python 2.7 and Pygame. Running on Android
requires a minimum of Android 2.2 (API 8).

License
-------

All the source code of Super HUGS Revolution 98 for Android is available under 
a FreeBSD style license. See the file "COPYING" for details.

All original graphic and audio content is available under the Creative Commons 
Public Domain Dedication. See http://creativecommons.org/publicdomain/zero/1.0/
for details.

The fonts in the font directory and the audio track TELEPORTER and associated
graphics are used under the terms of their respective licenses. Read the Aditional
Assets section further ahead for details.

The Forever Alone face and likeness is property of The Internet.

Compilation for Android
-----------------------

Super HUGS Revolution 98 depends on Python 2.7, Pygame, and pgs4a 0.9.4. Your
Python installation must have support for SQLite 3.

To compile Super HUGS Revolution for Android devices you need a
working instalation of Pygame Subset for Android (pgs4a) by
Tom Rothamel and Patrick Dawson. pgs4a can be
found at the following link:

    http://pygame.renpy.org/

Follow this steps to compile the game (instructions for GNU/Linux systems):

    1) cd to the pgs4a directory.
    2) Execute "./android.py configure Super-HUGS-Revolution-98".
    3) Answer the questions that will appear on the terminal. Press enter
       to use the default answers (between brackets []).
    4) Execute "./android.py build Super-HUGS-Revolution-98 release".

This will produce an installable .apk file inside the bin directory of pgs4a.
Compiling on Windows systems is similar.

Installation
------------

To install Super HUGS Revolution on an Android device, use adb:

    adb install Super-HUGS-Revolution-98-X.Y.apk

You can also compile and install with the following command:

    ./android.py build Super-HUGS-Revolution-98 release install

How to play
-----------

Executing:
To play on a PC execute the main.py script of Super HUGS Revolution 98. To play
on Android start the installed app (it is named HUGS by default).

Controls:
Guide Moncho by tapping and holding on the screen wherever you want him to
move to. On a PC just click with the mouse.

Scoring:
Hug people to increase your score. Every 25 hugs increases the current wave.
Enemies become more frequent on higher waves. Hug as many people as you can
before the time runs out.

Aditional assets
----------------

Super HUGS Revolution 98 uses the track "TELEPORTER" by Danjyon Kimura. The song
is available under a Creative Commons BY-NC-SA license 
(see http://creativecommons.org/licenses/by-nc-sa/3.0/) in
http://www.jamendo.com/es/list/a91205/8bit-easter

The fonts Press Start 2P and Profaisal-EliteRiqa are available in
http://openfontlibrary.org Check the font directory for more information
on the fonts.
