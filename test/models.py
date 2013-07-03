from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import dumper


class SimpleModel(models.Model):
    slug = models.CharField(max_length=200, default='slug')

    def get_absolute_url(self):
        return reverse('simple-detail', kwargs={'slug': self.slug})

    def dependent_paths(self):
        yield self.get_absolute_url()
        for model in self.related_set.all():
            yield model.get_absolute_url()


class RelatedModel(models.Model):
    slug = models.CharField(max_length=200, default='slug')
    related = models.ManyToManyField(SimpleModel, related_name='related_set')

    def dependent_paths(self):
        yield self.get_absolute_url()

    def get_absolute_url(self):
        return reverse('related-detail', kwargs={'slug': self.slug})


class GenericRelationModel(models.Model):
    slug = models.CharField(max_length=200, default='slug')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def dependent_paths(self):
        yield self.content_object.get_absolute_url()


class RelatedToGenericModel(models.Model):
    slug = models.CharField(max_length=200, default='slug')
    generic_related = generic.GenericRelation(GenericRelationModel)

    def get_absolute_url(self):
        return reverse('related-to-generic-detail', kwargs={'slug': self.slug})


class GenericRelationNotRegisteredModel(models.Model):
    slug = models.CharField(max_length=200, default='slug')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def dependent_paths(self):
        pass

dumper.register(SimpleModel)
dumper.register(RelatedModel)
dumper.register(GenericRelationModel)
