Warning: Don't use yet. I am still ironing out the kinks of invalidating
ManyToMany Models

django-dumper
============================

.. image:: https://pypip.in/v/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://travis-ci.org/saulshanabrook/django-dumper.png
    :target: https://travis-ci.org/saulshanabrook/django-dumper

.. image:: https://coveralls.io/repos/saulshanabrook/django-dumper/badge.png?branch=master
    :target: https://coveralls.io/r/saulshanabrook/django-dumper


``django-dumper`` allows view caching invalidation based on model saves.
It won't actually cache anything, but only invalidate the django cache.


Installation
------------

Installation is as easy as::

    pip install django-dumper

Then configure either the `per site` or `per view` cache.

.. _per site: https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache
.. _per view: https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache


Usage
-----
To invalidate certain paths on a model save, register that model using
``dumper.site.register``.

.. code-block:: python

    from django.db import models

    import dumper


    class SimpleModel(models.Model):
        slug = models.CharField(max_length=200)

        def get_absolute_url(self):
            return '/' + self.slug

        def dependent_paths(self):
            '''Returns a list of paths to invalidate when this model is updated'''
            return [self.get_absolute_url()]


    dumper.register(SimpleModel)

When a registered model is saved, ``dumper`` invalidates the caches returned
by the ``dependent_paths`` method of that model.

Contributing
------------

If you find issues or would like to see a feature suppored, head over to
the `issues section` and report it. Go ahead, do it!

.. _issues section: https://github.com/saulshanabrook/django-dumper/issues

To contribute code in any form, fork the repository and clone it locally.
Create a new branch for your feature::

    git commit -b feature/whatever-you-like

Then make sure all the tests past (and write new ones for any new features)::

    pip install -e .
    pip install -r requirements-dev.txt
    django-admin.py test --settings=test.settings

Check if the README.rst looks right::

    restview -e 'python setup.py --long-description'

Then push the finished feature to github and open a pull request form the branch.

New Release
^^^^^^^^^^^
To create a new release:

1. Add changes to ``CHANGES.txt``
2. Change version in ``setup.py``
3. ``python setup.py register``
4. ``python setup.py sdist upload``
