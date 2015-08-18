# Create your views here.

from django.http import HttpResponse
from PhoenixDev.PhoenixWebService.User.models import *


def product_ratings(request, product_id):
    x = Users.objects.all()


    return HttpResponse('Hello world' + ','.join([i.userName for i in x]))

    


