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

famulus [OPTIONS]

DESCRIPTION
===========

`famulus(1)` is a tool to run non-regression tests on a remote device.

OPTIONS
=======

-V, --version   display program version and exit
-D, --debug     show debug messages

ENVIRONMENT VARIABLES
=====================

Setting the following environment variables may alter the behavior of
`famulus(1)`:

- FAMULUS_LOG: logging level (DEBUG, WARNING)
- FAMULUS_SHOW_STACK_TRACES: if set, show Python stack trace on error.
