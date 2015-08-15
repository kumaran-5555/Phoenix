from django.db import models

# Create your models here.
class TestTable(models.Model):
    productName = models.CharField(max_length=20)

class ProductRatings(models.Model):
    # change to forieng key
    productId = models.IntegerField(unique=True)
    # change to forieng key
    userId = models.IntegerField(unique=True)
    ratingVal = models.IntegerField()

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateField(auto_now_add=True)

class ProductReview(models.Model):
    # change to forieng key
    productId = models.IntegerField(unique=True)
    # change to forieng key
    userId = models.IntegerField(unique=True)
    reviewVal = models.CharField(max_length=1024)

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateField(auto_now_add=True)

class SellerRating(models.Model):
    # change to forieng key
    sellerId = models.IntegerField(unique=True)
    # change to forieng key
    userId = models.IntegerField(unique=True)
    ratingVal = models.IntegerField()

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateField(auto_now_add=True)

class SellerReview(models.Model):
    # change to forieng key
    sellerId = models.IntegerField(unique=True)
    # change to forieng key
    userId = models.IntegerField(unique=True)
    reviewVal = models.CharField(max_length=1024)

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateField(auto_now_add=True)




