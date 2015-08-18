# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound


def signup(request):
    if request.method != 'POST':
        return HttpResponseNotFound()



