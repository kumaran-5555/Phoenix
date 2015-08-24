# Create your views here.

from django.http import HttpResponse
from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from django.db import IntegrityError

from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings




def rate_product(request):
    
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))


    productId = request.POST.get('productId', False)

    if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    ratingVal = request.POST.get('ratingVal', False)

    if not ratingVal or not ratingVal.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidRatingValue, ratingVal))

    ratingVal = int(ratingVal)
    productId = int(productId)
    
    if ratingVal < 0 or ratingVal > 5:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidRatingValue, ratingVal))


    try:
        product = Product.models.Products.objects.get(id = productId)

    except Product.models.Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    # session is validate, safe to take userId from session
    Product.models.ProductRatings.objects.create(productId = product, userId = request.session['userId'], ratingVal = ratingVal)
    

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, ''))

def review_product(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))


    productId = request.POST.get('productId', False)

    if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    reviewVal = request.POST.get('reviewVal', False)

    if not reviewVal:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidRatingValue, reviewVal))

    productId = int(productId)
    
    # validate review, avoid overflow
    reviewVal = reviewVal[:1024]

    try:
        product = Product.models.Products.objects.get(id = productId)

    except Product.models.Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    # session is validate, safe to take userId from session
    Product.models.ProductReview.objects.create(productId = product, userId = request.session['userId'], reviewVal = reviewVal)
    

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, ''))




