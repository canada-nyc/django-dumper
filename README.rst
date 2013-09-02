django-dumper
============================

.. image:: https://pypip.in/v/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://pypip.in/d/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://travis-ci.org/saulshanabrook/django-dumper.png
    :target: https://travis-ci.org/saulshanabrook/django-dumper

``django-dumper`` allows view caching invalidation based on model saves.
It won't actually cache anything, but only invalidate the django cache.
It is useful if your views are only dependent on model data. For instance,
a detail view will always return the same response, until the model changes.
So this response for thie view can be cached until the model is changed.


Why...?
-------
``django-dumper`` was created to scratch a rather specific itch. I was having
trouble reducing load times on pages where there were lots of images. By
default, if you want to render an image's url, width, and height, in a template then
that hits the storage backend three times per image. With a remote backend,
like S3, this creates long and unreliable page load times. If you are smarter
and create `cached height and width fields`_, then you can reduce this to one
hit. This is still not ideal for a page with 100+ images. So I thought, the only
time these images ever change, is when a model saves. And then I started
thinking, actually the only time any of my pages changed was when a model
saved. Of course, I still wanted my page load times to be as low as possible
before caching, but why would i re-render these pages on every request, if
they would be identical for every visitor, until someone changed a model?

So I set about to build an app that would allow me to do just that. It
would cache the full content of each response indefinitely. It would then
invalidate certain responses, based on their paths, whenever a model was saved.
For instance, if the ``/ice-cream/`` page displays links to each flavor and
``/ice-cream/<flavor-name>/`` has detailed information on a flavor, then
every time a flavor is saved, it should not only invalidate its specific detail
page, but also the general list page. This is definitely a brute force approach,
but it makes sense to me because it is *safe*. You might over invalidate, but,
if setup correctly, you will never have stale caches.

This is by no means an all purpose caching app. Every page rendered by your site
must be determined only by models. Detail and list views are examples of pages
determined by models. Also, if your site differentiates at based on request
headers (cookies, languages, etc...) then this will not work, because it will
serve the same version to all visitors.

.. _cached height and width fields: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ImageField.height_field



Installation
------------
Installation is as easy as::

    pip install django-dumper


Setup
-----
Configuration is similar to Django's `per site`_ cache.

You’ll need to add ``'dumper.middleware.cache.UpdateCacheMiddleware'`` and
``'dumper.middleware.cache.FetchFromCacheMiddleware'`` to your
``MIDDLEWARE_CLASSES setting``, as in this example:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'dumper.middleware.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'dumper.middleware.FetchFromCacheMiddleware',
    )

Then, add the following optional settings to your Django settings file:

1. ``DUMPER_CACHE_ALIAS`` – The cache alias to use for storage. Defaults
   ``'default'``
2. ``DUMPER_KEY_PREFIX`` – If the cache is shared across multiple sites
   using the same Django installation, set this to the name of the site,
   or some other string that is unique to this Django instance, to
   prevent key collisions. Defaults to ``'dumper.cached_path.'``.
3. ``DUMPER_PATH_IGNORE_REGEX`` – If matched on the path, then
   these pages will not be cached. By default it won't cached the admin
   ``^/admin/``

.. _per site: https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache

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


Advice
------
I would recommend enabling `ETags`_. That way the whole response
won't have to be sent to the user, only the header, if the ETAG is the same.

.. _ETags: https://docs.djangoproject.com/en/dev/ref/settings/#use-etags

The Django document ion does not cohesively describe how your middleware
should be ordered, however `this stack overflow`_ discussion does a fine job.

.. _this stackoverflow: http://stackoverflow.com/questions/4632323/practical-rules-for-django-middleware-ordering#question


Internals
---------
So you wanna know how this all works huh? Well it might seem pretty simple.
This library really has two parts. The first hooks into model saves and calls
and invalidation function on all the paths returned by ``dependent_paths``.
The second actually invalidates those paths.

Model Registration
^^^^^^^^^^^^^^^^^^
When you register a model, it connects a function that retrieves the paths
from the model and invalidates those paths to three signals. The first two
are ``post_save`` and ``pre_delete``, which make sense. The third is
``m2m_changed``. This signal is called actually by a ``through`` attribute of
a ``ManyToManyField`` and is called whenever any member of that relationship is
added added, deleted, or changed. It hooks this signal unto all the
many to many fields on the registered model. It most likely calls the
invalidation function more than once if a many to many relationship is changed,
but I figured there is minimal harm in over invalidating the paths, besides
a slight performance hit from hitting the cache backend. However I figured
this was worth it to maintain code simplicity.

Path Cache Invalidation
^^^^^^^^^^^^^^^^^^^^^^^
The cache keys for paths have been greatly simplified to only care about
two things when creating a key for a cached page. Those things are its
path and its method. So one path can have two different cached versions,
one for when it called with the ``HEAD`` method and one for the ``GET``
method.


Contributing
------------

If you find issues or would like to see a feature suppored, head over to
the `issues section` and report it. Don't be agraid, go ahead, do it!

.. _issues section: https://github.com/saulshanabrook/django-dumper/issues

To contribute code in any form, fork the repository and clone it locally.
Create a new branch for your feature::

    git commit -b feature/whatever-you-like

Then make sure all the tests past (and write new ones for any new features)::

    pip install -e .
    pip install -r requirements-dev.txt
    django-admin.py test --settings=test.settings

Check if the README.rst looks right::

    restview --long-description

Then push the finished feature to github and open a pull request form the branch.

New Release
^^^^^^^^^^^
To create a new release:

1. Add changes to ``CHANGES.txt``
2. Change version in ``setup.py``
3. ``python setup.py register``
4. ``python setup.py sdist upload``
