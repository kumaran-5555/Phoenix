# Create your views here.

# Create your views here.

from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from PhoenixDev.PhoenixWebService.Seller.models import *
from PhoenixDev.PhoenixWebService.Bargain.models import *
from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
import json
import sympy.geometry as geo

def send(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))


    selectionType = request.POST.get('selectionType', False)

    if selectionType is False:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSelectionType, selectionType))

    productId = None
    brandId = None
    categoryId = None
    
    if selectionType == Helpers.Constants.SelectionType.Product:
        productId = request.POST.get('productId', False)
        if productId is False:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

    elif selectionType == Helpers.Constants.SelectionType.Brand:
        brandId = request.POST.get('brandId', False)
        if brandId is False:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandId, brandId))
    elif selectionType == Helpers.Constants.SelectionType.Category:
        categoryId = request.POST.get('categoryId', False)
        if categoryId is False:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryID, categoryId))
    else:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSelectionType, selectionType))



    interestedInSimilar = request.POST.get('interestedInSimilar', False) != False


    latitude = request.POST.get('latitude', False)
    longitude = request.POST.get('longitude', False)


     # http://stackoverflow.com/questions/6536232/validate-latitude-and-longitude
    if not latitude:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidLatitude, latitude))
    try:
        latitude = float(latitude)
    except ValueError:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidLatitude, latitude))

    if latitude < -90 or latitude > 90:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidLatitude, latitude))



    if not longitude:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidLongitude, longitude))
    try:
        longitude = float(longitude)
    except ValueError:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidLongitude, longitude))

    if longitude < -180 or longitude > 180:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidLongitude, longitude))

    # TODO - search radius
    tiles = Helpers.overlapping_tiles(latitude, longitude)







    