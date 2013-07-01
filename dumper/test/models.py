from django.db import models
from django.core.urlresolvers import reverse


import dumper


class SimpleModel(models.Model):
    slug = models.CharField(max_length=200, default='slug')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def dependent_paths(self):
        return [self.get_absolute_url()]


dumper.register(SimpleModel)
