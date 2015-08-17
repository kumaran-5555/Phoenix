# Create your views here.

from django.http import HttpResponse


def product_ratings(request, product_id):
    return HttpResponse('Hello world')

