fpaste
------
fpaste is a command-line front-end for the Fedora Pastebin service at
fpaste.org.  It allows easy uploading of multiple files, or of copy&pasted
text from stdin, without requiring a web browser. A unique fpaste link is
returned, which can then be given to others who are offering help.

.. code:: bash

    e.g.:
    [joeuser@localhost ~]$ fpaste /etc/httpd/conf/httpd.conf
    Uploading...
    http://fpaste.org/rorn/


Upstream
========

The source code is hosted at https://pagure.io/fpaste where primary development will occur. Please file issues here. A mirror is also maintained at https://github.com/sanjayankur31/fpaste where you can open pull requests.

Why?
====

- PRIMARY: users don't like being flooded with large amounts of text, and
  encourage the use of pastebin sites & utilities instead.
- A GUI browser like firefox might be inaccessible.
- A TUI browser like lynx might be too cumbersome.
- Multiple files can be fpasted.
- It's often faster & more convenient to use the cli than to copy/paste in a
  browser's textarea.
- Why not?


Who?
====

fpaste maintainer:
    Jason 'zcat' Farrell <farrellj a gmail.com>
Server-side fpaste.org ninja:
    Jonathan 'daMaestro' Steffan <jon a fedoraunity.org>
Mr. FUPT - http://fedorasolved.org/Members/khaytsus/fedora-unity-paste-tool
    Walter 'Khaytsus' Francis <wally a theblackmoor.net>
Inspiration from ye olde bash script. R.I.P. rafb.net/paste
    Ignacio Vazquez-Abrams <ivazqueznet a gmail.com>
