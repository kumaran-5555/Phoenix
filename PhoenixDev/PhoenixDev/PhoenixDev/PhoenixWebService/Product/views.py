# Create your views here.

from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings
from django.db import IntegrityError
from django.http import HttpResponse
import json


def product_specs(request):

     # Validate if its a GET request 
     if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))
    
     ## Allow only if the user session is active
     #if not Helpers.validate_user_session(request):
     #   return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))
     
     productId = request.GET.get('productId')

     # Validate the product ID
     if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

     try:
        product = Products.objects.get(id = productId)

     except Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

     
     try :
        brand = ProductBrands.objects.get(id = product.productBrandId_id)

     except ProductBrands.DoesNotExist:
         return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandId, { "BrandId": product.productBrandId_id } ))

     # Populate Product Name and Brand Name since they are available at this point

     allDetailsDict = dict()
     allDetailsDict['Product Name'] = product.productName
     allDetailsDict['Brand Name']   = brand.brandName

     # TODO : Move the below two lines to product listing method 
     allDetailsDict['Product Min Price'] = str(product.productMinPrice)
     allDetailsDict['Product Max Price'] = str(product.productMaxPrice)

     # Filter to fetch multiple objects as opposed to get
     try :
         specs = ProductSpecs.objects.filter(productId_id=productId)

     except ProductSpecs.DoesNotExist :
         return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoSpecsFound, ''))

     # Iterate all Key Value pairs for this product and display the specs
     for spec in specs :
        allDetailsDict[spec.key] =  str(spec.value)
        
     return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, allDetailsDict))


def product_list(request):
    
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

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
        product = Products.objects.get(id = productId)

    except Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    # session is validated, safe to take userId from session
    ProductRatings.objects.create(productId = product, userId = request.session['userId'], ratingVal = ratingVal)
    

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




