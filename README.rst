Django Conversation
===================

A reusable Django app that provides threaded conversations between users.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-conversation

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/bitmazk/django-conversation.git#egg=conversation

TODO: Describe further installation steps (edit / remove the examples below):

Add ``conversation`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'conversation',
    )

Add the ``conversation`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^conversation/', include('conversation.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate conversation


Usage
-----

...


Settings
--------

...


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-conversation
    $ python setup.py install
    $ pip install -r dev_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
