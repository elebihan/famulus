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

famulus run [OPTIONS] <URI> <name> [<name>, ...]

famulus show [OPTIONS] {suite|test} <name>

DESCRIPTION
===========

`famulus(1)` is a tool to run non-regression tests on a remote machine.

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

run [OPTIONS] <URI> <name> [<name>, ...]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run one or more tests/suites on target identified by its URI, which format is
<scheme>://<resource>. The support schemes are:

- *ssh*: interact with the target via SSH. The resource is either a FQDN or an
  IP address, associated with an username and a password. Example:
  "ssh://foo:secret@192.168.0.1".
- *stty*: interact with the target via a serial TTY. On Posix systems, the
  resource is the path to the character device of the serial TTY, associated
  with the credentials ("stty://foo:secret@/dev/ttyS0"). On Microsoft Windows,
  it is the name of serial port ("stty://foo:secret@/COM4").
- *telnet*: interact with the target via Telnet (RFC 854). The resource is
  either a FQDN or an IP address, associated with an username and a password.
  Example: "telnet://foo:secret@192.168.0.1".
- *uboot*: interact with the target running U-Boot, connected via serial port.
  The resource is the same as for "stty", but no credentials are required.
  Examples: "uboot:///dev/ttyS0", "uboot:///COM4".

Credentials are fetched from the configuration file when omitted in the URI.

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

EXAMPLES
========

Run suites "foo" and "baz" on machine whose IP address is 192.168.0.1 via SSH::

  $ famulus run ssh://192.168.0.1 foo baz

SEE ALSO
========

- famulus.conf(5)
