=======
famulus
=======

-------------------
servile test runner
-------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2016 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

famulus [OPTIONS] <command> [<argument>,...]

famulus list [OPTIONS] {suites|tests}

DESCRIPTION
===========

`famulus(1)` is a tool to run non-regression tests on a remote device.

OPTIONS
=======

-V, --version             display program version and exit
-C FILE, --config FILE    set path to configuration file
-D, --debug               show debug messages

COMMANDS
========

The following commands are available:

list [OPTIONS] {suites|tests}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the available tests or test suites.

ENVIRONMENT VARIABLES
=====================

Setting the following environment variables may alter the behavior of
`famulus(1)`:

- FAMULUS_LOG: logging level (DEBUG, WARNING)
- FAMULUS_SHOW_STACK_TRACES: if set, show Python stack trace on error.
