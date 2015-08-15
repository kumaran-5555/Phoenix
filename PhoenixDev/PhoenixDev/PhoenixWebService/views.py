# Create your views here.
from django.http import HttpResponse
from .models import TestTable


def index(request):
    rows = TestTable.objects.all()
    line = ','.join([r.productName for r in rows])
    return HttpResponse("Hello, world. You're at the polls index." + line)

def productRatings(request, product_id=None):
    return HttpResponse(str(product_id) + " Recieved product_id")
