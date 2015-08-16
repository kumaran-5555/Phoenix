﻿from django.db import models


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
    # let db add timestamp, we use now + expiary in business logic to compute
    # expiaryTimestamp
    expiaryTimestamp = models.DateTimeField() 
  
class BargainOfferedFeatures(models.Model):
    '''
        store what features seller offered for a
        bargain request
    '''
    bargainId = models.ForeignKey(BargainResponse)
    featureId = models.ForeignKey(AvailableFeatures)
        

