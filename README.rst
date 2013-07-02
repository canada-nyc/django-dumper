django-dumper
============================

.. image:: https://pypip.in/v/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://travis-ci.org/saulshanabrook/django-dumper.png
    :target: https://travis-ci.org/saulshanabrook/django-dumper

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
To invalidate certain paths on a model save and delete, register that model
using ``dumper.register``. It will invalidate every path returned by the
``dependent_paths`` method.

.. code-block:: python

    from django.db import models

    import dumper


    class IceCream(models.Model):
        slug = models.CharField(max_length=200)

        def get_absolute_url(self):
            return '/' + self.slug

        def dependent_paths(self):
            '''Returns a list of paths to invalidate when this model is updated'''
            return [self.get_absolute_url()]

    dumper.register(IceCream)

``dependent_paths`` can also returns the paths of related objects to invalidate
them as well. For instance if each ``IceCream`` had some related ``Sizes``
then if one of those sizes is modified, that should invalidate the ``IceCream``
as well.


.. code-block:: python

    from django.db import models

    import dumper


    class IceCream(models.Model):
        slug = models.CharField(max_length=200)
        sizes = models.ManyToManyField(Size, related_name='ice_creams')

        def get_absolute_url(self):
            return '/' + self.slug

        def dependent_paths(self):
            '''Returns a list of paths to invalidate when this model is updated'''
            return [self.get_absolute_url()]


    class Size(models.Model):
        slug = models.CharField(max_length=200)

        def get_absolute_url(self):
            return '/' + self.slug

        def dependent_paths(self):
            for ice_cream in self.ice_creams:
                yield ice_cream.get_absolute_url()
            yield self.get_absolute_url()

    dumper.register(IceCream)
    dumper.register(Size)

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
