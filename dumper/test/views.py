from django.http import HttpResponse

from .models import SimpleModel


def detail(request, slug):
    model = SimpleModel.objects.get(slug=slug)
    return HttpResponse(model.slug)
