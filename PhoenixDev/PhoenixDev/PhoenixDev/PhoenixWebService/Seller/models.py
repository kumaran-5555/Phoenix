﻿from django.db import models


from PhoenixDev.PhoenixWebService import *

class Sellers(models.Model):
    '''
        primary table to store seller information
    '''
    sellerName = models.CharField(max_length=100)
    sellerCityName = models.CharField(max_length=50)
    sellerAddress = models.CharField(max_length=300)
    sellerPrimaryPhone = models.CharField(max_length=11, unique=True)
    sellerSecondaryPhone = models.CharField(max_length=11)
    sellerLatitude = models.FloatField()
    sellerLongitude = models.FloatField()
    sellerMailId = models.CharField(max_length=100)
    sellerWebsite = models.CharField(max_length=100)
    # short description of seller sells or about seller
    sellerDescription = models.CharField(max_length=1024)
    # let the backend add the timestamp during creation
    sellerSingupTimestamp = models.DateTimeField(auto_now_add=True)
    sellerPasswordHash = models.CharField(max_length=512)
    sellerTileId = models.CharField(max_length=20)
    sellerAppId = models.CharField(max_length=Helpers.Constants.appIdLength, default='')

    # python pickle-d dict of features
    sellerRankingFeatures = models.BinaryField(2048, default=None)



class SellerOTPMappings(models.Model):
    '''
        stores the otp send to a mobile number for validating 
        again
    '''
    phoneNumber = models.CharField(max_length=10)
    otpValue = models.CharField(max_length=5)
    expiaryDate = models.DateTimeField()


class SellerRating(models.Model):
    '''
        user seller review
    '''
    # change to forieng key
    sellerId = models.ForeignKey(Sellers)
    # change to forieng key
    userId = models.ForeignKey(User.models.Users)
    ratingVal = models.IntegerField()

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)

class SellerReview(models.Model):
    '''
        user seller rating
    '''
    # change to forieng key
    sellerId = models.ForeignKey(Sellers)
    # change to forieng key
    userId = models.ForeignKey(User.models.Users)
    reviewVal = models.CharField(max_length=1024)

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)