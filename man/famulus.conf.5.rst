============
famulus.conf
============

------------------------------
Configuration file for Famulus
------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2016 Eric Le Bihan
:Manual section: 5

DESCRIPTION
===========

The ``famulus.conf`` file contains the configuration parameters for
`famulus(1)`. It uses a structure similar to Microsoft Windows INI files.

The default location for this file is ``~/.config/famulus.conf``.

SYNTAX
======

The file contains sections, led by a *[section]* header followed by
*key=value* pairs. Lines beginning with '#' are considered as comments.

Example::

  # Configuration file
  [General]
  Editor = emacsclient
  TestsPaths = /some/location,/another/one

SECTIONS
========

Here is the list of potential sections, as well as the supported options.

General
-------

* Editor: the text editor to use
* TestsPaths: comma separated list of paths to test/suite files

Connection
----------

* Username: name to use for connection
* Password: password to use for connection

SEE ALSO
========

- ``famulus(1)``
