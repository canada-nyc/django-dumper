django-dumper
============================

.. image:: https://pypip.in/v/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://pypip.in/d/django-dumper/badge.png
        :target: https://crate.io/packages/django-dumper

.. image:: https://travis-ci.org/saulshanabrook/django-dumper.png
    :target: https://travis-ci.org/saulshanabrook/django-dumper

``django-dumper`` provides full site caching, similar to Django's,
along with path based invalidation based on model saves.
It will cache every page that is not in ``DUMPER_PATH_IGNORE_REGEX``
**forever**. So for it to be effective, all of your pages must
be invalidated when neccesary, by specifying in your models
which paths should be invalidated those models are saved.


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

.. hint:: If you use Django Grappelli, then you shouldn't be caching
   any paths under `/grappelli/` and if you are serving media or static from
   your app, you should ignore those as well.

   .. code-block:: python

        DUMPER_PATH_IGNORE_REGEX = r'^/(?:(?:admin)|(?:grappelli)|(?:media))/'

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


Debugging
---------
The `dumper` package has `DEBUG` logging in place for the midleware
and for the invalidation. To enable this, just make sure that
any logs coming from `dumper` with the level `DEBUG` are shown.

The simplest way to do this would be to this in your `settings.py`

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'name': {
                'format': '%(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'name'
            },
        },
        'loggers': {
            'dumper': {
                'level': 'DEBUG',
                'handlers': ['console', ]
            }
        }
    }



Advice
------
I would recommend enabling `ETags`_. That way the whole response
won't have to be sent to the user, only the header, if the ETAG is the same.

.. _ETags: https://docs.djangoproject.com/en/dev/ref/settings/#use-etags

The Django document ion does not cohesively describe how your middleware
should be ordered, however `this stack overflow`_ discussion does a fine job.

.. _this stack overflow: http://stackoverflow.com/questions/4632323/practical-rules-for-django-middleware-ordering#question


Internals
---------

Cache Middleware |dumper/middleware.py|_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
My caching is based off of Django's `per site cache`_, but much simpler.
Originally I just used their cache, but this greatly complicated my code
and made it harder to understand. This is because their cache
`creates different cached versions`_. for the same URL based on the ``Vary`` HTML header.
It is much more complicated to implement path based invalidation, if other things
besides the path are being use to generate the cache key. For instance, when I was
supporting the Django middleware I had to figure out a way to delete every cached
version of the path.

If your pages do vary based on anything besides the path and HTTP method,
then you should not cache them with ``django-dumper``. Either ignore them
with the ``DUMPER_PATH_IGNORE_REGEX`` setting or don't use the project at all
if all of your pages fall under this category.

.. |dumper/middleware.py| replace:: ``dumper/middleware.py``
.. _dumper/middleware.py: https://github.com/saulshanabrook/django-dumper/blob/master/dumper/middleware.py
.. _per site cache: https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache
.. _creates different cached versions: https://github.com/django/django/blob/master/django/middleware/cache.py#L38-L39


Invalidate Paths |dumper/invalidation.py|_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to invalidate a model when it saves, we get the path's that should
be invalidated from the model, and then remove the cache keys that correspond
to those paths. Each cache key is made up of a path plus a HTTP method.

.. |dumper/invalidation.py| replace:: ``dumper/invalidation.py``
.. _dumper/invalidation.py: https://github.com/saulshanabrook/django-dumper/blob/master/dumper/invalidation.py


Invalidating on Model Saves: |dumper/site.py|_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When you register a model a invalidation function to three signals.
That function gets the paths from the model and then uses |dumper/invalidation.py|_
to delete them. The three signals it registers with are ``post_save``, ``pre_delete``,
and ``m2m_changed``. The last signal is called whenever any member that relationship
is added, deleted, or changed. It most likely calls the
invalidation function more than once if a many to many relationship is changed,
but is harmless, besides the slight performance hit from hitting the cache backend.

.. |dumper/site.py| replace:: ``dumper/site.py``
.. _dumper/site.py: https://github.com/saulshanabrook/django-dumper/blob/master/dumper/site.py


Contributing
------------

If you find issues or would like to see a feature suppored, head over to
the `issues section` and report it. Don't be agraid, go ahead, do it!

.. _issues section: https://github.com/saulshanabrook/django-dumper/issues

To contribute code in any form, fork the repository and clone it locally.
Create a new branch for your feature::

    git commit -b feature/whatever-you-like

Then make sure all the tests past (and write new ones for any new features)

With Fig and Docker::

    fig up
    # run fig build test if you change the required packages before testing again

Normally::

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


.. image:: https://d2weczhvl823v0.cloudfront.net/saulshanabrook/django-dumper/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

