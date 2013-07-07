django-dumper
============================

.. image:: https://pypip.in/v/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://travis-ci.org/saulshanabrook/django-dumper.png
    :target: https://travis-ci.org/saulshanabrook/django-dumper

``django-dumper`` allows view caching invalidation based on model saves.
It won't actually cache anything, but only invalidate the django cache.
It is useful if your views are only dependent on model data. For instance,
a detail view will always return the same response, until the model changes.
So this response for thie view can be cached until the model is changed.


Installation
------------
Installation is as easy as::

    pip install django-dumper


Setup
-----
Configure the `per site`_ cache.

Then replace ``django.middleware.cache.FetchFromCacheMiddleware``
and ``django.middleware.cache.UpdateCacheMiddleware``
with  ``dumper.middleware.FetchFromCacheMiddleware`` and
``dumper.middleware.UpdateCacheMiddleware``


.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'dumper.middleware.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'dumper.middleware.FetchFromCacheMiddleware',
    )

Note: dumper will not work with the `per view`_ cache. If you want this support
then submit an issue, it should not be too hard to implement.

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


Advice
------
You can set ``CACHE_MIDDLEWARE_SECONDS`` to a very long time, because each
of your URLs will be invalidated when the models change. However, currently
Django does not let you differentiate between backend and frontend caching.
For instance, if you set it to cache for a year, then the browser would also
be instructed to cache that page for a year, so even when the backend cache
is invalidated the cached browser version will remain outdated. I currently
don't have a solution for this, besides modifying the headers on each view
indivually. `This thread`_ on stackoverflow covers the problem.

.. _This thread: http://stackoverflow.com/questions/8448722/can-i-stop-djangos-site-wide-caching-middleware-from-setting-cache-control-and

I also would reccomend enabling `ETags`_. That way the whole response
won't have to be sent to the user, only the header, if the ETAG is the same.

.. _ETags: https://docs.djangoproject.com/en/dev/ref/settings/#use-etags

The Django documention does not cohesively describe how your middleware
should be ordered, however `this stackoverflow`_ discussion does a fine job.

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
You would think that invalidating a cache of a certain path shouldn't be too
hard, just look at how the middleware caches the response, get the same key
and then delete the cache entry for it. However the cache middleware varies
the cache based on a few different request headers, such as cookies attached
and language provided. This makes sense if you want your page responses to vary
at the same path. However it makes invalidation a pain. `Certain`_ `techniques`_
`used`_ `to`_ invalidate these paths simply create a mock request with the path
set to the path you want to invalidate, and gets the key using that request.
I originally attempted to implement it this way, but I quickly found that
it was difficult to test, because the test requests were different than the
actuall browser requests and so presented difficult to find bugs in
invalidation, where the cache might be invalidated for a path when accessing
the path in the tests, but when accessing it on the browser it wasn't
invalidated. Also it completely ignored different language caches, so if you
varied your responses at all based on language or any other header, then it
wouldn't invalidate your cache.

.. _Certain: http://stackoverflow.com/questions/720800/removing-specific-items-from-djangos-cache
.. _techniques: http://stackoverflow.com/questions/12574422/cant-delete-cache-for-specific-entry-in-django
.. _used: http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
.. _to: http://stackoverflow.com/questions/3346124/how-do-i-force-django-to-ignore-any-caches-and-reload-data

So instead I created a middleware that invalidates the cache key, based on
if it's path has already been invalidated since the last invalidation.
Read through `the source`_ for the details.

.. _the source: https://github.com/saulshanabrook/django-dumper/blob/master/dumper/invalidation.py

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
