from django.http import HttpResponse

from . import models


def simple_detail(request, slug):
    model = models.SimpleModel.objects.get(slug=slug)
    return HttpResponse(model.slug)


def related_detail(request, slug):
    model = models.RelatedModel.objects.get(slug=slug)
    related = model.related.all()
    related_unique = map(
        lambda related: related.slug + str(related.pk),
        related
    )
    return HttpResponse(' '.join(related_unique) + model.slug)


def related_to_generic_detail(request, slug):
    model = models.RelatedToGenericModel.objects.get(slug=slug)
    generic_related = model.generic_related.all()
    generic_related_unique = map(
        lambda generic_related: generic_related.slug + str(generic_related.pk),
        generic_related
    )
    return HttpResponse(' '.join(generic_related_unique) + model.slug)
