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
        'django_libs',
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

Please add the following files to your base.html

.. code-block:: html

    <link rel="stylesheet" href="{% static "conversation/css/conversation.css" %}">
    <script src="{% static "conversation/js/conversation.js" %}"></script>

The conversations in this app are threaded, that means a conversation is
related to one object. In this case the object is a user. So if ``user1``
starts a conversation with ``user2`` all messages between those users are
stored in one conversation (you know it, if your are e.g. a Facebook user).

This app allows another relation, so you can also add a content object to a
conversation between two users. Let's say you built a sports app. ``user1``
wants to talk with ``user2`` about a fight called ``Klitschko vs. Tyson``. They
can now start a conversation, which is also related to that fight. But, they
can also start a new conversation about other fights or talk to each other
without another relation, for sure.

If you have executed the tasks written above, the app is ready to work.
Note: The templates are based on Twitter Bootstrap (http://getbootstrap.com/).
If you don't use it, simply overwrite them.

In almost every case you want to customize stuff, add jQuery/JavaScript, add
CSS, your own templates and so on, so this app is kept very simple.


Settings
--------

CONVERSATION_MESSAGE_FORM
+++++++++++++++++++++++++

Default: None

If you want to use your own message form, you can define it here::

    CONVERSATION_MESSAGE_FORM = 'my_app.forms.MyMessageForm'



Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-conversation
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
