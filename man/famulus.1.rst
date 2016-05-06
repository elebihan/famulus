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

famulus edit [OPTIONS] {suites|tests} <name>

famulus list [OPTIONS] {suites|tests}

famulus new [OPTIONS] {suite|test} <name>

famulus run [OPTIONS] <name> [<name>, ...]

famulus show [OPTIONS] {suite|test} <name>

DESCRIPTION
===========

`famulus(1)` is a tool to run non-regression tests on a remote device.

OPTIONS
=======

-V, --version             display program version and exit
-C FILE, --config FILE    set path to configuration file
-D, --debug               show debug messages
-T DIR, --tests-path DIR  add path to tests/suites

COMMANDS
========

The following commands are available:

edit [OPTIONS] {suite|test} <name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Edit the specification of a test or suite.

list [OPTIONS] {suites|tests}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the available tests or test suites.

new [OPTIONS] {suite|test} <name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new test or test suite.

The default text editor set by the user via the *$EDITOR* environment variable
or from the configuration file will be summoned to edit the new file.

Available options:

-f NAME, --from=NAME    use NAME as template
-O DIR, --output=DIR    set output directory

run [OPTIONS] <name> [<name>, ...]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run one or more test/suite.

By default, the events occuring during the execution of a test/suite are
formatted in a human-friendly way. Use *--event-format=machine* to format them
for machine processing.

Available options:

-F FMT, --event-format=FMT    set event logging format

show [OPTIONS] {suite|test} <name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Print information about a test or a suite.

ENVIRONMENT VARIABLES
=====================

Setting the following environment variables may alter the behavior of
`famulus(1)`:

- FAMULUS_LOG: logging level (DEBUG, WARNING)
- FAMULUS_SHOW_STACK_TRACES: if set, show Python stack trace on error.
