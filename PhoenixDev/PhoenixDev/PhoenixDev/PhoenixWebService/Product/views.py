# Create your views here.

from PhoenixDev.PhoenixWebService.User.models import *
from PhoenixDev.PhoenixWebService.Product.models import *
from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
import json


def product_specs(request):

     # Validate if its a GET request 
     if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))
    
     # Allow only if the user session is active.
     if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))
     
     productId = request.GET.get('productId')

     # Validate the product ID
     if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

     try:
        product = Products.objects.get(id = productId)

     except Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

     
     try :
        brand = ProductBrands.objects.get(id = product.productBrandId_id)

     except ProductBrands.DoesNotExist:
         return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidBrandId, { "BrandId": product.productBrandId_id } ))

     # Populate Product Name and Brand Name since they are available at this point

     allDetailsDict = dict()
     allDetailsDict['Product Name'] = product.productName
     allDetailsDict['Brand Name']   = brand.brandName

     # Filter to fetch multiple objects as opposed to get
     try :
         specs = ProductSpecs.objects.filter(productId_id=productId)

     except ProductSpecs.DoesNotExist :
         return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoSpecsFound, ''))

     # Iterate all Key Value pairs for this product and display the specs
     for spec in specs :
        allDetailsDict[spec.key] =  str(spec.value)
        
     return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, allDetailsDict))


def product_reviews(request):

     # Validate if its a GET request 
     if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))
    
     # Allow only if the user session is active.
     if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))
     
     productId = request.GET.get('productId')

     # Validate the product ID
     if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))

     
     topNReviews = []
     startFound = request.GET.get('from')
     endFound   = request.GET.get('to')

      # Check if from/to parameters are set in GET request, else return 10 recent reviews by default
     if not startFound and not endFound :
         try:
            topNReviews = ProductReviews.objects.filter(productId_id=productId)[:Settings.DEFAULT_LISTING_COUNT]
            
         except ProductReviews.DoesNotExist :
             return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoReviewsFound, ''))
     
     if not startFound and endFound :
        try:
           end = int(endFound)
           topNProducts = ProductReviews.objects.filter(productId_id=productId)[:end]
           
        except ProductReviews.DoesNotExist :
             return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoReviewsFound, ''))

     sendReviews = []
     if startFound :
         start = int(startFound)

         if not endFound :

                try:
                    topNReviews = ProductReviews.objects.filter(productId_id=productId)[start : start + Settings.DEFAULT_LISTING_COUNT]
                    
                except ProductReviews.DoesNotExist:
                    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoReviewsFound, ''))
         else :
               # Both from and to are present
                end = int(endFound)

                try:
                    topNReviews = ProductReviews.objects.filter(productId_id=productId)[start : end]

                except ProductReviews.DoesNotExist:
                    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoReviewsFound, ''))
         
         
     for r in topNReviews :
         sendReviews.append(r.reviewVal)
        
     return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, sendReviews))
              

def product_list(request):
    
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    categoryId = request.GET.get('categoryId')

    # Validate the category ID
    if not categoryId or not categoryId.isdigit():
       return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryID, categoryId))


    startFound = request.GET.get('from')
    endFound   = request.GET.get('to')
    orderBy = ''

    # Can be extended to any kind of filtering/sorting based on Product Model attributes
    availableFilters = ['brandFilter', 'priceFilter']
    availableOrderings = ['popularity', 'reviewCount']

    # TODO : Use Q() objects to efficiently handle multiple filters and sortby.
    # for filter in availableFilters :
    #    if filter in request.GET.keys() :


    topNProducts = []
    # Check if from/to parameters are set in GET request, else return 10 popular products by default
    if not startFound and not endFound :
        try:
           topNProducts = Products.objects.filter(productCategoryId_id=categoryId)[:Settings.DEFAULT_LISTING_COUNT]
           
        except Products.DoesNotExist :
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoProductsFound, categoryId))


    if not startFound and endFound :
        try:
           end = int(endFound)
           topNProducts = Products.objects.filter(productCategoryId_id=categoryId)[:end]
           
        except Products.DoesNotExist :
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoProductsFound, categoryId))

    if startFound :
        start = int(startFound)

        if not endFound :

               try:
                   topNProducts = Products.objects.filter(productCategoryId_id=categoryId)[start : start + Settings.DEFAULT_LISTING_COUNT]
                    
               except Products.DoesNotExist:
                   return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoProductsFound, categoryId))
        else :
               # Both from and to are present
               end = int(endFound)

               try:
                   topNProducts = Products.objects.filter(productCategoryId_id=categoryId)[start : end]

               except Products.DoesNotExist:
                   return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoProductsFound, ''))
         
    
    sendNProducts = []

    for item in topNProducts :
        sendNProducts.append([item.productName, item.productMinPrice, item.productMaxPrice, item.productAvgRating] )
        
        
    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, sendNProducts))
     

    

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term        
    terms = Helpers.normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def product_search(request):

    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))

    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    query_string = ''

    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['productName'])

        try:
            # Search based on average rating
            found_entries = Products.objects.filter(entry_query).order_by('-productAvgRating')
                    
        except Products.DoesNotExist:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NoProductsFound, ''))
        
        
     
    entries = []
    for results in found_entries :
        entries.append(results.productName)

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, entries))


def rate_product(request):
    
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))


    productId = request.POST.get('productId', False)

    if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    ratingVal = request.POST.get('ratingVal', False)

    if not ratingVal or not ratingVal.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidRatingValue, ratingVal))

    ratingVal = int(ratingVal)
    productId = int(productId)
    
    if ratingVal < 0 or ratingVal > 5:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidRatingValue, ratingVal))


    try:
        product = Products.objects.get(id = productId)

    except Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    # session is validated, safe to take userId from session
    ProductRatings.objects.create(productId = product, userId = request.session['userId'], ratingVal = ratingVal)
    

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, ''))

def review_product(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))


    productId = request.POST.get('productId', False)

    if not productId or not productId.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    reviewVal = request.POST.get('reviewVal', False)

    if not reviewVal:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidRatingValue, reviewVal))

    productId = int(productId)
    
    # validate review, avoid overflow
    reviewVal = reviewVal[:1024]

    try:
        product = Product.models.Products.objects.get(id = productId)

    except Product.models.Products.DoesNotExist:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductId, productId))


    # session is validate, safe to take userId from session
    Product.models.ProductReview.objects.create(productId = product, userId = request.session['userId'], reviewVal = reviewVal)
    

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, ''))


def offerings_delete(request):

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))

    sellerId = request.session['sellerId']
    
    categoryIdList = request.POST.get('categoryIdList', False)

    productIdList = request.POST.get('productIdList', False)

    if not categoryIdList and not productIdList:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOfferingParams, ''))



def add_offerings(request):

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))
    
    categoryIdList = request.POST.get('categoryIdList', False)
    productIdList = request.POST.get('productIdList', False)
    sellerId = request.session['sellerId']

    if not categoryIdList and not productIdList:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOfferingParams, ''))

    catIdList = []
    cContents = categoryIdList.split(',')

    for c in cContents :
        try:
            catIdListInt.append(int(c))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryIdList, categoryIdList))

    prodIdList = []
    pContents = productIdList.split(',')

    for p in pContents:
        try:
            proIdList.append(int(p))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductIdList, productIdList))

    for c in catIdList :
        # if categoryId already exists, skip
        sentinel = SellerCategoryOfferings.filter(sellerId = sellerId, categoryId = c)
        if sentinel :
            cc = SellerCategoryOfferings.create(sellerId = sellerId, categoryId = c)

    for p in prodIdList :
        # if productId already exists, skip
        sentinel = SellerProductOfferings.filter(sellerId = sellerId, productId = p)
        if not sentinel :   
            pp = SellerProductOfferings.create(sellerId = sellerId, productId = p)

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'Added!'))



def offerings_delete(request):

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))

    sellerId = request.session['sellerId']
    
    categoryIdList = request.POST.get('categoryIdList', False)

    productIdList = request.POST.get('productIdList', False)

    if not categoryIdList and not productIdList:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOfferingParams, ''))

    categoryIdListInt = []

    fields = categoryIdList.split(',')

    for f in fields:
        try:
            categoryIdListInt.append(int(f))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCategoryIdList, categoryIdList))

    productIdListInt = []

    fields = productIdList.split(',')

    for f in fields:
        try:
            productIdListInt.append(int(f))
        except ValueError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidProductIdList, productIdList))

    for c in categoryIdListInt:
        row = Product.models.SellerCategoryOfferings.filter(sellerId = sellerId, categoryId = c).delete()

    for p in productIdListInt:
        row = Product.models.SellerProductOfferings.filter(sellerId = sellerId, productId = p).delete()


    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'deleted'))






