SNMP Watcher [![Build Status](https://travis-ci.org/muflone/snmp-watcher.svg?branch=master)](https://travis-ci.org/muflone/glivesnmp) [![Join the chat at https://gitter.im/muflone/glivesnmp](https://badges.gitter.im/muflone/glivesnmp.svg)](https://gitter.im/muflone/snmp-watcher?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
=====

**Description:** Watch devices through SNMP.

**Copyright:** 2018 Fabio Castelli (Muflone) <muflone(at)vbsimple.net>

**License:** GPL-2+

**Codice sorgente:** https://github.com/muflone/snmp-watcher

**Documentazione:** http://www.muflone.com/snmp-watcher/

System Requirements
-------------------

* Python 2.x (developed and tested for Python 2.7.5)
* XDG library for Python 2.x
* Distutils library for Python 2.x (usually shipped with Python distribution)
* PySNMP (<http://snmplabs.com/pysnmp/>)
* Tabulate (<https://bitbucket.org/astanin/python-tabulate>)

Installation
------------

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python2 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python2 setup.py install --root NEW_PATH

Usage
-----

If the application is not installed please use:

    cd /path/to/folder
    python2 snmp-watcher.py

If the application was installed simply use the snmp-watcher command.
