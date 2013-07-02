from django.http import HttpResponse

from .models import SimpleModel, RelatedModel


def simple_detail(request, slug):
    model = SimpleModel.objects.get(slug=slug)
    return HttpResponse(model.slug)


def related_detail(request, slug):
    model = RelatedModel.objects.get(slug=slug)
    related = model.related.all()
    related_unique = map(
        lambda related: related.slug + str(related.pk),
        related
    )
    return HttpResponse(' '.join(related_unique) + model.slug)
