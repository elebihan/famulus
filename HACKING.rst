==================
Hacking on famulus
==================

Localisation
============

To extract messages, use::

  $ PYTHONPATH=. ./setup.py extract_messages

To create a new catalog for locale <locale>, use::

  $ PYTHONPATH=. ./setup.py init_catalog --locale <locale>

To compile the catalog for locale <locale>, use::

  $ PYTHONPATH=. ./setup.py build_catalog --locale <locale>

To compile the all catalogs, use::

  $ PYTHONPATH=. ./setup.py build_catalog

To update the catalog for locale <locale>, use::

  $ PYTHONPATH=. ./setup.py update_catalog --locale <locale>
