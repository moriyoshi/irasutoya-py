============
Irasutoya-py
============

.. image:: https://travis-ci.org/moriyoshi/irasutoya-py.svg?branch=master

Irasutoya-py scrapes over www.irasutoya.com and fetchs information about illustrations provided there.


-----------------
Command-line tool
-----------------

Listing categories
------------------

::

    $ irasutoya categories


Listing all items in the category
---------------------------------


::

    $ irasutoya items CATEGORY


If you want the details for each illustration as well, give ``--with-details`` option to it.


::

    $ irasutoya items --with-details CATEGORY


