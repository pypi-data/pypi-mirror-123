=============================
Django Uploads App
=============================

.. image:: https://badge.fury.io/py/django-uploads-app.svg
    :target: https://badge.fury.io/py/django-uploads-app

.. image:: https://travis-ci.org/paiuolo/django-uploads-app.svg?branch=master
    :target: https://travis-ci.org/paiuolo/django-uploads-app

.. image:: https://codecov.io/gh/paiuolo/django-uploads-app/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/paiuolo/django-uploads-app

Django uploads manager

Documentation
-------------

The full documentation is at https://django-uploads-app.readthedocs.io.

Quickstart
----------

Install Django Uploads App::

    pip install django-uploads-app

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_uploads_app.apps.DjangoUploadsAppConfig',
        ...
    )

Add Django Uploads App's URL patterns:

.. code-block:: python

    from django_uploads_app import urls as django_uploads_app_urls


    urlpatterns = [
        ...
        url(r'^', include(django_uploads_app_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
