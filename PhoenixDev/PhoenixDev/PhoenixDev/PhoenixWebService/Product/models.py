from django.db import models
from PhoenixDev.PhoenixWebService import *


class CategoryTaxonomy(models.Model):
    '''
        root category ID is 0
        captures category navigation

    '''
    parentCategory = models.ForeignKey('CategoryTaxonomy')
    categoryName = models.CharField(max_length=200)

class ProductBrands(models.Model):
    '''
        captures brand-category mapping,
        we can use this is sending bargain request to 
        selected seller who offer a specific brand in that category
    '''
    brandName = models.CharField(max_length=200)
    categoryId = models.ForeignKey(CategoryTaxonomy)

class Products(models.Model):
    '''
        primary table to store product information
        specs are stored in ProductSpecs key-value style
    '''
    # auto primary key is created by django, we will use that
    # TODO - supports more than category 
    productCategoryId = models.ForeignKey(CategoryTaxonomy)
    productName = models.CharField(max_length=200)
    productMinPrice = models.IntegerField()
    productMaxPrice = models.IntegerField()
    productBrandId = models.ForeignKey(ProductBrands)




class SellerProductOfferings(models.Model):
    '''
        we allow seller to fill this or we will learn from his/her
        bargain replies
    '''
    sellerId = models.ForeignKey(Seller.models.Sellers)
    productId = models.ForeignKey(Products)

class SellerCategoryOfferings(models.Model):
    '''
        seller offerings of product categories
    '''
    sellerId = models.ForeignKey(Seller.models.Sellers)
    categoryId = models.ForeignKey(CategoryTaxonomy)

class SellerBrandOfferings(models.Model):
    '''
        seller offerings of brands
    '''
    sellerId = models.ForeignKey(Seller.models.Sellers)
    brandId = models.ForeignKey(ProductBrands)


class ProductSpecs(models.Model):
    '''
        stores specs for all products as key value pairs
    '''
    productId = models.ForeignKey(Products)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=1024)



class ProductRatings(models.Model):
    '''
        user given ratings for each product
    '''
    # change to forieng key
    productId = models.ForeignKey(Products)
    # change to forieng key
    userId = models.ForeignKey(User.models.Users)
    ratingVal = models.IntegerField()

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)

class ProductReview(models.Model):
    '''
        user product review
    '''
    # change to forieng key
    productId = models.ForeignKey(Products)
    # change to forieng key
    userId = models.ForeignKey(User.models.Users)
    reviewVal = models.CharField(max_length=1024)

    # let the backend add the timestamp during creation
    ratingTimestamp = models.DateTimeField(auto_now_add=True)