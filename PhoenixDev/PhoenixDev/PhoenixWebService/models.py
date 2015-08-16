from django.db import models

# Create your models here.
class TestTable(models.Model):
    productName = models.CharField(max_length=20)


class Sellers(models.Model):
    sellerName = models.CharField(max_length=100)
    sellerCityName = models.CharField(max_length=50)
    sellerAddress = models.CharField(max_length=300)
    sellerPrimaryPhone = models.CharField(max_length=11)
    sellerSecondaryPhone = models.CharField(max_length=11)
    sellerLatitute = models.FloatField()
    sellerLongitude = models.FloatField()
    sellerMailId = models.CharField(max_length=100)
    sellerWebsite = models.CharField(max_length=100)
    # short description of seller sells or about seller
    sellerDescription = models.CharField(max_length=1024)
    # let the backend add the timestamp during creation
    sellerSingupTimestamp = models.DateTimeField(auto_now_add=True)
    sellerPasswordHash = models.CharField(max_length=512)

class Products(models.Model):
    # auto primary key is created by django, we will use that
    # TODO - supports more than category 
    productCategoryId = models.ForeignKey('CategoryTaxonomy')
    productName = models.CharField(max_length=200)
    productMinPrice = models.IntegerField()
    productMaxPrice = models.IntegerField()
    productBrandName = models.ForeignKey('ProductBrands')

class ProductBrands(models.Model):
    brandName = models.CharField(max_length=200)
    categoryId = models.ForeignKey('CategoryTaxonomy')


class SellerProductOfferings(models.Model):
    '''
        we allow seller to fill this or we will learn from his/her
        bargain replies
    '''
    sellerId = models.ForeignKey('Sellers')
    productId = models.ForeignKey('Products')


class CategoryTaxonomy(models.Model):
    '''
        root category ID is 0
    '''
    parentCategory = models.ForeignKey('CategoryTaxonomy')
    categoryName = models.CharField(max_length=200)

class ProductSpecs(models.Model):
    '''
        stores specs for all products as key value pairs
    '''
    productId = models.ForeignKey('Products')
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=1024)



class ProductRatings(models.Model):
    # change to forieng key
    productId = models.ForeignKey('Products')
    # change to forieng key
    userId = models.ForeignKey('Users')
    ratingVal = models.IntegerField()

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)

class ProductReview(models.Model):
    # change to forieng key
    productId = models.ForeignKey('Products')
    # change to forieng key
    userId = models.ForeignKey('Users')
    reviewVal = models.CharField(max_length=1024)

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)

class SellerRating(models.Model):
    # change to forieng key
    sellerId = models.ForeignKey('Sellers')
    # change to forieng key
    userId = models.ForeignKey('Users')
    ratingVal = models.IntegerField()

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)

class SellerReview(models.Model):
    # change to forieng key
    sellerId = models.ForeignKey('Sellers')
    # change to forieng key
    userId = models.ForeignKey('Users')
    reviewVal = models.CharField(max_length=1024)

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)


class Users(models.Model):
    userName = models.CharField(max_length=100)
    userPrimaryPhone = models.CharField(max_length=11)
    userMailId = models.CharField(max_length=100)
    # For completion sake, these fields can be optional for user.
    userCityName = models.CharField(max_length=50)
    userAddress = models.CharField(max_length=300)
    # sha512
    userPasswordHash = models.CharField(max_length=512)
    userSignupTime = models.DateTimeField(auto_now_add=True)

class BargainRequest(models.Model):
    userId = models.ForeignKey('Users')
    productId = models.ForeignKey('Products')
    searchLatitude = models.FloatField()
    searchLongitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # let db add timestamp, we use now + expiary in business logic to compute
    # expiaryTimestamp
    expiaryTimestamp = models.DateTimeField() 
    sharePhone = models.BooleanField()
    comment = models.CharField(max_length=256)
    requestedPrice = models.IntegerField()

class BargainReqeustedFeatures(models.Model):
    '''
        stores what features user wanted during a 
        product bargain 
    '''
    baragainId = models.ForeignKey('BargainRequest')
    featureId = models.ForeignKey('AvailableFeatures')


class BargainResponse(models.Model):
    bargainRequestId = models.ForeignKey('BargainRequest')
    sellerId = models.ForeignKey('Sellers')
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
    bargainId = models.ForeignKey('BargainResponse')
    featureId = models.ForeignKey('AvailableFeatures')




class AvailableFeatures(models.Model):
    '''
        has per product category features that users 
        can choose during bargain request
    '''
    # TODO - right now all features all boolean type, support more types

    featureCategoryId = models.ForeignKey('CategoryTaxonomy')
    featureName = models.CharField(max_length=200)



