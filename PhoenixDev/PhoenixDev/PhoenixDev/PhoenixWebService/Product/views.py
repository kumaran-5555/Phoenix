# Create your views here.

from django.http import HttpResponse
from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from PhoenixDev.PhoenixWebService import Helpers
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


def product_ratings(request, product_id):
    x = Users.objects.all()


    return HttpResponse('Hello world' + ','.join([i.userName for i in x]))



    


