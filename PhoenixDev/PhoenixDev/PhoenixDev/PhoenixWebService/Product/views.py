# Create your views here.

from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings
from django.db import IntegrityError
from django.http import HttpResponse
import json


def product_specs(request):

    product_id = request.GET.get('product_id');
    product = Products.objects.get(id=product_id)
    brand = ProductBrands.objects.get(id=product.productBrandId_id)
    detailsDict = {}
    detailsDict['Product Name'] = product.productName
    detailsDict['Brand Name'] = brand.brandName
    detailsDict['Product Min Price'] = str(product.productMinPrice)
    detailsDict['Product Max Price'] = str(product.productMaxPrice)

    specs = ProductSpecs.objects.filter(productId_id=product_id)

    for spec in specs :
        detailsDict.add(spec.key, str(spec.value))
        
    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success,detailsDict))


def product_list(request):
    
    paramsDict = {"sortname" : "popularity", "sortvalue" : "descending"}
    getParamDict = request.GET
     
    listOfParams = ['start','end','filtername1','filtervalue1', 'filtername2','filtervalue2','category_id']
    
    #for param in listOfParams:
    #    if param in getParamDict.keys() and param not in paramsDict.keys() :
    #            paramsDict[param] = getParamDict[param]
    #    elif param in getParamDict.keys() and param in paramsDict.keys() :
    #            paramsDict[param] = getParamDict[param]
    #    else :
    #        #exception
    #        raise AssertionError
    products = Products.objects.filter(productCategoryId_id='6')
    for product in products :
        relatedProductRatings = product.productratings_set.all()
        for prodRating in relatedProductRatings :
            print prodRating.ratingVal    
    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success,relatedInfo))

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




