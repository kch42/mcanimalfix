mcanimalfix
===========

This tool will place animals in your Minecraft map, if there are no animals existing.
This can happen to old maps after upgrading to Minecraft >= Beta 1.8.

It tries to simulate the standard Minecraft animal spawning mechanism.
Spawning wolves is a bit problematic, they only spawn in forest biomes, but it is
(IMHO) not possible to read out the used biome for a chunk. So this tool tries to figure out
where a forest could be (where are many trees?).

WARNING!
--------

Before you do this, PLEASE backup your Map. I could not see any problems, but just in case...

Requirements
------------

* Python 2.x (<http://www.python.org>)
* pymclevel (<https://github.com/codewarrior0/pymclevel>. Just place the pymclevel into the root directory of this tool)
* numpy (Needed by pymclevel. <http://numpy.scipy.org/>)
* wxPython (<http://wxpython.org/>. Make sure you use an Unicode-enabled version!)

Usage
-----

Launch `animalfix.py`, select the directory of your Minecraft map and click "Lets do it!".
Then you have to wait quite a long time. My map is ~ 50 MiB large and it took about 15 minutes to fix it (running on Fedora 14 with an Phenom II X4 965).

EXE version for Windows
-----------------------

There is an EXE file for Windows (32-bit, should also work on 64-bit), so you do not have to download Python and tons of other software.
Just unzip the archive and execute mcanimalfix.exe.
Download: <https://github.com/downloads/kch42/mcanimalfix/mcanimalfix_win32.zip>

License
-------

NOTE: pymclevel is not my work. It was originally witten by codewarrior0. See <https://github.com/codewarrior0/pymclevel/blob/master/LICENSE.txt> for pymclevel's license.

Now mcanimalfix' license:

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2004 Sam Hocevar
 14 rue de Plaisance, 75014 Paris, France
Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.

