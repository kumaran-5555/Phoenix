# Create your views here.

# Create your views here.

from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from PhoenixDev.PhoenixWebService.Seller.models import *
from PhoenixDev.PhoenixWebService.Bargain.models import *
from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
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
    
    # we should get either one of these
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



    if productId is None and brandId is None and categoryId is None:
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


    message = request.POST.get('message', False)
    if not message or not Helpers.validateMessage(message):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBargainMessage, message))


    # TODO - search radius
    tiles = Helpers.overlapping_tiles(latitude, longitude)

    # we user selected product, we will send notification to potential
    # all sellers who sells this product, this brand and this category
    # in ranking, we use whether user is interested in similar product or 
    # not to truncate

    if productId:
        row = Product.models.Products.objects.get(id=productId)
        brandId = row.brandId_id

        row = Product.models.ProductBrands.objects.get(id=brandId)
        categoryId = row.categoryId_id

    elif brandId:
        row = Product.models.ProductBrands.objects.get(id=brandId)
        categoryId = row.categoryId_id

    
    routes = []

    if productId:
        routes.append([(t, productId, Helpers.Constants.SelectionType.Product) for t in tiles])

    if brandId:
        routes.append([(t, brandId, Helpers.Constants.SelectionType.Brand) for t in tiles])

    if categoryId:
        routes.append([(t, categoryId, Helpers.Constants.SelectionType.Category) for t in tiles])


    sellers = []
    for r in routes:
        rows = Bargain.models.MessageRouter.objects.filter(tileId = r[0], productSelectionId = r[1], productSelectionType = r[2])
        for s in rows:
            sellers.append(s)

    # do some ranking
    sellers = Helpers.rankeSellers(sellers)


    # create message
    messageObj = Bargain.models.MessageBox.objects.create(userId=request.session.get('userId'), headMessage=message)

    
    shortMessage = Helpers.shortenMessage(message)

    for seller in sellers:
        # add message for seller

        # create threads
        Bargain.models.MessageBoxThreads(messageId = messageObj, fromId = request.session.get('userId'), toId = seller.sellerId, message=message)

        Bargain.models.NotificationsQueue.create(appId=seller.sellerAppId, shortMessage=shortMessage)


    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'numOfSeller': len(sellers)}))





def close(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    messageId = request.POST.get('messageId', False)

    try:
        message = Bargain.models.MessageBox.objects.get(id=messageId)
    except ObjectDoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, ''))


    if message.userId != request.session.get('userId'):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'notOwner' : messageId }))
    

    
    message.isActive = False

    message.save()

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'deletedMessageId': messageId}))


def view_summary(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))


    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    userId = request.session.get('userId')

    messages = Bargain.models.MessageBox.objects.filter(userId=userId).oder_by('recentResponseTimestamp').desc()


    skip = request.GET.get('skip', False)

    if not skip:
        skip = 0

    else:
        try:
            skip = int(skip)
        except ValueError:
            skip = 0

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'messages' : messages[skip: skip + Helpers.Constants.numMesssagesToReturn]}))



    
def view_details(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))


    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    userId = request.session.get('userId')

    messageId = request.GET.get('messageId', False)

    if not messageId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'messageId': messageId}))


    # we already have head message, only has to retrive response

    messages = Bargain.models.MessageBoxThreads.objects.filter(messageId=messageId, toId=userId).order_by('timestamp').desc()

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, { 'messages': messages}))





   












    