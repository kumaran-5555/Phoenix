from django.db import models
from PhoenixDev.PhoenixWebService import *


class BargainRequest(models.Model):
    '''
        immutable bargain request created by the user
    '''
    userId = models.ForeignKey(User.models.Users)
    productId = models.ForeignKey(Product.models.Products)
    searchLatitude = models.FloatField()
    searchLongitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # let db add timestamp, we use now + expiary in business logic to compute
    # expiaryTimestamp
    expiaryTimestamp = models.DateTimeField() 
    sharePhone = models.BooleanField()
    comment = models.CharField(max_length=256)
    requestedPrice = models.IntegerField()


class AvailableFeatures(models.Model):
    '''
        has per product category features that users 
        can choose during bargain request
    '''
    # TODO - right now all features all boolean type, support more types

    featureCategoryId = models.ForeignKey(Product.models.CategoryTaxonomy)
    featureName = models.CharField(max_length=200)


class BargainReqeustedFeatures(models.Model):
    '''
        stores what features user wanted during a 
        product bargain 
    '''
    baragainId = models.ForeignKey(BargainRequest)
    featureId = models.ForeignKey(AvailableFeatures)


class BargainResponse(models.Model):
    '''
        immutable bargain response created by the seller
    '''
    bargainRequestId = models.ForeignKey(BargainRequest)
    sellerId = models.ForeignKey(Seller.models.Sellers)
    offeredPrice = models.IntegerField()
    comment = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    # let db add timestamp, we use now + expiry in business logic to compute
    # expiaryTimestamp
    expiaryTimestamp = models.DateTimeField() 
  

class BargainOfferedFeatures(models.Model):
    '''
        store what features seller offered for a
        bargain request
    '''
    bargainId = models.ForeignKey(BargainResponse)
    featureId = models.ForeignKey(AvailableFeatures)
        

class MessageBox(models.Model):
    # skip FK to user
    userId = models.IntegerField(11)
    timestamp = models.DateTimeField(auto_now_add=True)
    headMessage = models.CharField(max_length=1024)
    recentResponseTimestamp = models.DateTimeField(auto_now=True)
    recentResponse = models.CharField(max_length=1024)
    numOfResponses = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)
    userAppId = models.CharField(max_length=Helpers.Constants.appIdLength, default='')
    


class MessageBoxThreads(models.Model):
    '''
        stores raw message
    '''
    messageId = models.ForeignKey(MessageBox)

    # skip FK
    fromId = models.IntegerField(11)
    # skip FK
    toId = models.IntegerField(11)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=4096)


class MessageRouter(models.Model):
    '''
       provides routing information for message
       given product/category/brand+category + location
       provides sellers who are likely to fullfill the request 
    '''

    # skip FK
    tileId = models.CharField(max_length=20)
    # captures product/brand/category Ids
    productSelectionId = models.IntegerField(11)
    # prodvides what type of selection product/brand/category
    productSelectionType = models.IntegerField()

    # skip FK
    sellerId = models.IntegerField(11)
    # helps easy re-tiling
    sellerLatitude = models.FloatField()
    sellerLongitude = models.FloatField()
    # python pickle-d dict of features
    sellerRankingFeatures = models.BinaryField(2048,default=None)

    # seller appid for sending notification
    sellerAppId = models.CharField(max_length=Helpers.Constants.appIdLength, default='')



    

class NotificationsQueue(models.Model):
    appId = models.CharField(max_length=Helpers.Constants.appIdLength, default='')
    shortMessage = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)
    retryCount = models.IntegerField(default=0)
    isPending = models.BooleanField(default=True)



