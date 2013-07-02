from django.db import models
from django.core.urlresolvers import reverse


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


dumper.register(SimpleModel)
dumper.register(RelatedModel)
