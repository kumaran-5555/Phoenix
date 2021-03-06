﻿# Create your views here.

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



def send(request):

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))


    selectionType = request.POST.get('selectionType', False)

    if selectionType is False:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSelectionType, selectionType))

    try:
        selectionType = int(selectionType)
    except ValueError:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSelectionType, selectionType))


    
    productId = None
    brandId = None
    categoryId = None
    
    # we should get either one of these
    if selectionType == Helpers.Constants.SelectionType.Product:
        productId = request.POST.get('productId', False)
        if productId is False:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

        try:
            productId = int(productId)
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

    elif selectionType == Helpers.Constants.SelectionType.Brand:
        brandId = request.POST.get('brandId', False)
        if brandId is False:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandId, brandId))

        try:
            brandId = int(brandId)
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandId, brandId))


    elif selectionType == Helpers.Constants.SelectionType.Category:
        categoryId = request.POST.get('categoryId', False)
        if categoryId is False:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryID, categoryId))

        try:
            categoryId = int(categoryId)
        except ValueError:
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

    Helpers.logger.debug('overlapping tiles {0}'.format('\t'.join(tiles)))

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

    
    Helpers.logger.debug('productId {} brandId {} categoryId {}'.format(productId, brandId, categoryId))

    routes = []

    if productId:
        routes.extend([(t, productId, Helpers.Constants.SelectionType.Product) for t in tiles])

    if brandId:
        routes.extend([(t, brandId, Helpers.Constants.SelectionType.Brand) for t in tiles])

    if categoryId:
        routes.extend([(t, categoryId, Helpers.Constants.SelectionType.Category) for t in tiles])


    Helpers.logger.debug('Routes {}'.format('\t'.join([str(t) for t in routes])))
    sellers = []
    sellerIds = {}
    for r in routes:
        rows = Bargain.models.MessageRouter.objects.filter(tileId = r[0], productSelectionId = r[1], productSelectionType = r[2])
        for s in rows:
            if s.sellerId in sellerIds:
                continue

            sellerIds[s.sellerId] = True

            sellers.append(s)

    Helpers.logger.debug('Sellers {}'.format('\t'.join([str(s.sellerId) for i in sellers])))

    user = request.session.get('userId')

    # do some ranking
    sellers = Helpers.rankeSellers(sellers)


    # create message
    messageObj = Bargain.models.MessageBox.objects.create(userId=user.id, headMessage=message, userAppId=user.userAppId)

    
    shortMessage = Helpers.shortenMessage(message)

    for seller in sellers:
        # add message for seller

        # create threads
        Bargain.models.MessageBoxThreads.objects.create(messageId = messageObj, fromId = user.id, toId = seller.sellerId, message=message)

        Bargain.models.NotificationsQueue.objects.create(appId=seller.sellerAppId, shortMessage=shortMessage)


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


    user = request.session.get('userId')
    if message.userId != user.id:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'notOwner' : messageId }))
    

    
    message.isActive = False

    message.save()

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'deletedMessageId': messageId}))


def view_summary(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))


    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    userId = request.session.get('userId').id

    messages = Bargain.models.MessageBox.objects.filter(userId=userId).order_by('recentResponseTimestamp').reverse()


    skip = request.GET.get('skip', False)

    if not skip:
        skip = 0

    else:
        try:
            skip = int(skip)
        except ValueError:
            skip = 0

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'messages' : Helpers.jsonizeDjangoObject(messages[skip: skip + Helpers.Constants.numMesssagesToReturn])}))



    
def view_details(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))


    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    userId = request.session.get('userId').id

    messageId = request.GET.get('messageId', False)

    if not messageId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'messageId': messageId}))


    try:
        messageId = int(messageId)
    except valueError:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'messageId': messageId}))



    # we already have head message, only has to retrive response

    messages = Bargain.models.MessageBoxThreads.objects.filter(Q(messageId=messageId) & (Q(toId=userId) | Q(fromId=userId))).order_by('timestamp').reverse()

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, { 'messages': Helpers.jsonizeDjangoObject(messages)}))





   
def reply(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))


    seller = request.session['sellerId']
    
    messageId = request.POST.get('messageId', False)


    if not messageId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'messageId': messageId}))

    try:
        messageId = int(messageId)
    except valueError:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMessageId, {'messageId': messageId}))

    message = request.POST.get('message', False)

    if not message or not Helpers.validateMessage(message):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBargainMessage, message))
    

    toId = request.POST.get('toId', False)

    if not toId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidToid, {'messageId': toId}))

    try:
        toId = int(toId)
    except valueError:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidToid, {'messageId': toId}))

    try:
        messageObj = Bargain.models.MessageBox.objects.get(id=messageId)

    except ObjectDoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InactiveMessage, {'messageId': messageId}))



    if messageObj.userId != toId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidToid, {'messageId': toId}))

    if not messageObj.isActive:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InactiveMessage, {'messageId': messageId}))


    

    shortMessage = Helpers.shortenMessage(message)

    # update message details
    messageObj.numOfResponses += 1
    messageObj.recentResponse = shortMessage


    messageObj.save()


    # create threads
    Bargain.models.MessageBoxThreads.objects.create(messageId = messageObj, fromId = seller.id, toId = toId, message=message)

    Bargain.models.NotificationsQueue.objects.create(appId=messageObj.userAppId, shortMessage=shortMessage)
 

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'Replied!'))





def seller_view_details(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))


    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))

    sellerId = request.session['sellerId'].id

   

    skip = request.GET.get('skip', False)

    if not skip:
        skip = 0

    else:
        try:
            skip = int(skip)
        except ValueError:
            skip = 0



    # we already have head message, only has to retrive response

    messages = Bargain.models.MessageBoxThreads.objects.filter((Q(toId=sellerId) | Q(fromId=sellerId))).order_by('timestamp').reverse()[skip:skip+20]

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, { 'messages': Helpers.jsonizeDjangoObject(messages)}))





   

def add_offerings(request):

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))
    
    categoryIdList = request.POST.get('categoryIdList', False)
    productIdList = request.POST.get('productIdList', False)
    brandIdList = request.POST.get('brandIdList', False)
    seller = request.session['sellerId']
    
   
    if not categoryIdList and not productIdList and not brandIdList:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOfferingParams, ''))

    catIdList = []
    if categoryIdList:
        cContents = categoryIdList.split(',')
    else:
        cCoutents = []

    for c in cContents :
        try:
            catIdList.append(int(c))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryIdList, categoryIdList))

    prodIdList = []
    if productIdList:
        pContents = productIdList.split(',')
    else:
        pContents = []

    for p in pContents:
        try:
            prodIdList.append(int(p))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductIdList, productIdList))


    branIdList = []
    if brandIdList:
        bContents = brandIdList.split(',')
    else:
        bContents = []

    for p in bContents:
        try:
            branIdList.append(int(p))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandIdList, brandIdList))




    for c in catIdList :
        # validate existence

        try:
            row = Product.models.CategoryTaxonomy.objects.get(id=c)
        except ObjectDoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryIdList, c))

        # if categoryId already exists, skip
        sentinel = Bargain.models.MessageRouter.objects.filter(sellerId = seller.id, productSelectionId = c, productSelectionType = Helpers.Constants.SelectionType.Category)
        if not sentinel :
            cc = Bargain.models.MessageRouter.objects.create(tileId = seller.sellerTileId, sellerId = seller.id, productSelectionId = c, productSelectionType = Helpers.Constants.SelectionType.Category, \
                sellerLatitude = seller.sellerLatitude, sellerLongitude = seller.sellerLongitude, sellerRankingFeatures = seller.sellerRankingFeatures, \
                sellerAppId = seller.sellerAppId)


    for p in prodIdList :
        try:
            row = Product.models.Products.objects.get(id=p)
        except ObjectDoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductIdList, p))

        # if categoryId already exists, skip
        sentinel = Bargain.models.MessageRouter.objects.filter(sellerId = seller.id, productSelectionId = p, productSelectionType = Helpers.Constants.SelectionType.Product)
        if not sentinel :
            cc = Bargain.models.MessageRouter.objects.create(tileId = seller.sellerTileId, sellerId = seller.id, productSelectionId = p, productSelectionType = Helpers.Constants.SelectionType.Product, \
                sellerLatitude = seller.sellerLatitude, sellerLongitude = seller.sellerLongitude, sellerRankingFeatures = seller.sellerRankingFeatures, \
                sellerAppId = seller.sellerAppId)

    for b in branIdList:
        try:
            row = Product.models.ProductBrands.objects.get(id=b)
        except ObjectDoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandIdList, b))


        # if categoryId already exists, skip
        sentinel = Bargain.models.MessageRouter.objects.filter(sellerId = seller.id, productSelectionId = b, productSelectionType = Helpers.Constants.SelectionType.Brand)
        if not sentinel :
            cc = Bargain.models.MessageRouter.objects.create(tileId = seller.sellerTileId, sellerId = seller.id, productSelectionId = b, productSelectionType = Helpers.Constants.SelectionType.Brand, \
                sellerLatitude = seller.sellerLatitude, sellerLongitude = seller.sellerLongitude, sellerRankingFeatures = seller.sellerRankingFeatures, \
                sellerAppId = seller.sellerAppId)

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'Added!'))



def delete_offerings(request):

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))

    categoryIdList = request.POST.get('categoryIdList', False)
    productIdList = request.POST.get('productIdList', False)
    brandIdList = request.POST.get('brandIdList', False)
    seller = request.session['sellerId']


    if not categoryIdList and not productIdList and not brandIdList:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOfferingParams, ''))

    catIdList = []
    cContents = categoryIdList.split(',')

    for c in cContents :
        try:
            catIdList.append(int(c))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryIdList, categoryIdList))

    prodIdList = []
    pContents = productIdList.split(',')

    for p in pContents:
        try:
            prodIdList.append(int(p))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductIdList, productIdList))


    branIdList = []
    bContents = brandIdList.split(',')

    for p in bContents:
        try:
            branIdList.append(int(p))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandIdList, brandIdList))




    for c in catIdList :
        # validate existence

        try:
            row = Product.models.CategoryTaxonomy.objects.get(id=c)
        except ObjectDoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryIdList, c))

        # if categoryId exists, delete
        sentinel = Bargain.models.MessageRouter.objects.filter(sellerId = seller.id, productSelectionId = c, productSelectionType = Helpers.Constants.SelectionType.Category).delete()
        


    for p in prodIdList :
        try:
            row = Product.models.Products.objects.get(id=p)
        except ObjectDoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductIdList, p))

        # if categoryId already exists, skip
        sentinel = Bargain.models.MessageRouter.objects.filter(sellerId = seller.id, productSelectionId = p, productSelectionType = Helpers.Constants.SelectionType.Product).delete()

    for b in branIdList:
        try:
            row = Product.models.ProductBrands.objects.get(id=b)
        except ObjectDoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandIdList, b))


        # if categoryId already exists, skip
        sentinel = Bargain.models.MessageRouter.objects.filter(sellerId = seller.id, productSelectionId = b, productSelectionType = Helpers.Constants.SelectionType.Brand).delete()
       

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'Deleted!'))





