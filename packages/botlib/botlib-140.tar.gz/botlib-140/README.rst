README
######

**BOTLIB** is an attempt to achieve OS level integration of bot technology
directly into the operating system. A solid, non hackable bot, that stores
it's data as JSON files on disk, every object is timestamped, readonly of 
which the latest is served to the user layer.  File paths carry the type in
the path name what makes reconstruction from filename easier then reading
type from the object.  This bot is intended to be  programmable in a static, 
only code, no popen, no imports and no reading  modules from a directory.

For programming the bot you have to have the code available as employing
your own code requires that you install your own bot as the system bot, as
to not have a directory to read modules from to add commands to the bot but
include the own programmed modules directly into the python code. This way 
only trusted code (your own written code) is included and runnable, reading
random code from a directory is what gets avoided.

Only run your own written code should be the path to "secure".

COMMANDS
========

fetch the code from https://pypi.org/project/botlib/#files

untar the tarball, cd into the bot directory and add your module to the bot
packages:

 > joe bot/hlo.py

add your command code to the file:

 >>> def hlo(event):
 >>>     event.reply("hello!")

then add bot/hlo.py to the bot/all.py module and let it scan the module.

 >>> import bot.hlo as hlo
 >>> Table.addmod(hlo)

bot.all is a module that is imported in the program, this makes
programming the library accessing sys.path instead of reading modules from
disk. So ..

1) add file to bot package
2) add file to bot/all.py

COPYRIGHT
=========

**BOTLIB** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

Bart Thate
