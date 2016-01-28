import json
import logging
import re
import math
import PhoenixDev.PhoenixWebService.Settings

from django.utils import timezone
import datetime
from PhoenixDev.PhoenixWebService import *
from django.core import serializers



logger = logging.getLogger(Settings.LOGGERNAME)

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError




class Constants():
    class SelectionType:
        Product = 0
        Brand = 1
        Category = 2
    latLongModulo = 5
    latLongMultiplyer = 100
    numMesssagesToReturn = 10
    appIdLength = 512


class StatusCodes():
    # have two members per code
    Success = 0
    InvalidPhoneNum = 1
    InvalidOtpValue = 2
    NotPostRequest = 3
    OtpValidationFailed = 4
    # while user creating password
    InvalidPassword = 5
    PhoneNumAlreadyExists = 6
    InvalidUsernamePassword = 7
    NotGetRequest = 8
    InvalidUserSession = 9
    InvalidProductId = 10
    InvalidRatingValue = 11
    InvalidBrandId = 12
    NoSpecsFound = 13
    NoReviewsFound = 14
    InvalidSellerName = 15
    InvalidCityName = 16
    InvalidAddress = 17
    InvalidLatitude = 18
    InvalidLongitude = 19
    InvalidMailId = 20
    InvalidWebsite = 21
    InvalidDescription = 22
    InvalidSellerSession = 23
    NoProductsFound = 24
    InvalidCategoryID = 25
    InvalidOfferingParams = 26
    InvalidProductIdList = 27
    InvalidCategoryIdList = 28
    InvalidSelectionType =  29
    InvalidBargainMessage = 30
    InvalidMessageId = 31
    InvalidBrandIdList = 32
    InvalidAppId = 33
    InvalidToid = 34
    InactiveMessage = 35

    


class StatusMessage():
    statusMessages = {}
    statusMessages[StatusCodes.InvalidPhoneNum] = 'Invalid phone number'
    statusMessages[StatusCodes.InvalidOtpValue] = 'Invalid otp value'
    statusMessages[StatusCodes.NotPostRequest] = 'Not post request'
    statusMessages[StatusCodes.Success] = 'Success'
    statusMessages[StatusCodes.OtpValidationFailed] ='Otp validation failed'
    statusMessages[StatusCodes.InvalidPassword] = 'Password is invalid'
    statusMessages[StatusCodes.PhoneNumAlreadyExists] = 'Phonenumber already exists'
    statusMessages[StatusCodes.InvalidUsernamePassword] = 'Invalid user name password'
    statusMessages[StatusCodes.NotGetRequest] = 'Not get request'
    statusMessages[StatusCodes.InvalidUserSession] = 'Invalid user session'
    statusMessages[StatusCodes.InvalidProductId] = 'Invalid product id'
    statusMessages[StatusCodes.InvalidRatingValue] = 'Invalid rating value'
    statusMessages[StatusCodes.InvalidBrandId] = 'Invalid brand id'
    statusMessages[StatusCodes.NoSpecsFound] = 'Specs not found for the product'
    statusMessages[StatusCodes.NoReviewsFound] = 'Reviews not found for the product'
    statusMessages[StatusCodes.InvalidSellerName] = 'Invalid seller name'
    statusMessages[StatusCodes.InvalidCityName] = 'Invalid city name'
    statusMessages[StatusCodes.InvalidAddress] = 'Invalid address'
    statusMessages[StatusCodes.InvalidLatitude] = 'Invalid latitude'
    statusMessages[StatusCodes.InvalidLongitude] = 'Invalid longitude'
    statusMessages[StatusCodes.InvalidMailId] = 'Invalid mail id'
    statusMessages[StatusCodes.InvalidWebsite] = 'Invalid website'
    statusMessages[StatusCodes.InvalidDescription] = 'Invalid description'
    statusMessages[StatusCodes.InvalidSellerSession] = 'Invalid seller session'
    statusMessages[StatusCodes.NoProductsFound] = 'No products found'
    statusMessages[StatusCodes.InvalidCategoryID] = "Invalid Category ID"
    statusMessages[StatusCodes.InvalidOfferingParams] = "Invalid delete offering params"
    statusMessages[StatusCodes.InvalidCategoryIdList] = "Invalid category Id List"
    statusMessages[StatusCodes.InvalidSelectionType] = "Invalid selection type"
    statusMessages[StatusCodes.InvalidBargainMessage] = 'Invalid Bargain message'
    statusMessages[StatusCodes.InvalidMessageId] = 'Invalid message id'
    statusMessages[StatusCodes.InvalidBrandIdList] = 'Invalid brand id list'
    statusMessages[StatusCodes.InvalidAppId] = 'Invalid app id'
    statusMessages[StatusCodes.InvalidToid] = 'Invalid to id'
    statusMessages[StatusCodes.InactiveMessage] = 'Inactive message'













def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

    



def create_json_output(statusCode, data):

    output = {}

    if statusCode not in StatusMessage.statusMessages:
        raise NotImplementedError
    
    output['status'] = { 'statusCode' : statusCode, 'statusMessage' : StatusMessage.statusMessages[statusCode] }
    output['data'] = data

    return json.dumps(output)




def create_user_session(request, phoneNumber, userId):
    '''
        creates session in request, assumes valid userId and phoneNumber
    '''

    # cleanup session
    request.COOKIES = {}
    request.session.flush()


    # set session 
    request.session['phoneNumber'] = phoneNumber
    request.session['userId'] = User.models.Users.objects.get(id=userId)
    request.session['loggedInTime'] = timezone.now()
    request.session['lastActivityTime'] = timezone.now()
    request.session['type'] = Settings.USER_TYPE
    

     


def validate_user_session(request):
    '''
        validates session and updates timestamps
        if required

        returns boolean
    '''
    
    if request.session.get('userId', False):
        # update last activity in steps
        # every x mins update last activity, this is to keep session active
        now = timezone.now()
        delta = datetime.timedelta(Settings.USER_SESSION_UPDATE_TIME)


        lastActivity = request.session.get('lastActivityTime', False)
        if not lastActivity:
            # looks like the session is broken
            # TODO clear the session
            logger.debug('Broken session')
            # remove bad sessions - this fixed in the later version. Happy !
            request.COOKIES = {}
            request.session.flush()

            return False
        
        if lastActivity + delta < now:
            request.session['lastActivityTime'] = timezone.now()       
        

        return True
    # remove bad sessions - this fixed in the later version. Happy !
    request.COOKIES = {}
    request.session.flush()

    return False

def delete_user_session(request):
    '''
        assumes session is valid
    '''
    request.session.flush()






def create_seller_session(request, phoneNumber, sellerId):
    '''
        creates session in request, assumes valid sellerId and phoneNumber
    '''

    # cleanup session
    request.COOKIES = {}
    request.session.flush()


    # set session 
    request.session['phoneNumber'] = phoneNumber
    request.session['sellerId'] = Seller.models.Sellers.objects.get(id=sellerId)
    request.session['loggedInTime'] = timezone.now()
    request.session['lastActivityTime'] = timezone.now()
    request.session['type'] = Settings.SELLER_TYPE


    
def validate_seller_session(request):
    '''
        validates session and updates timestamps
        if required

        returns boolean
    '''
    
    if request.session.get('sellerId', False):
        # update last activity in steps
        # every x mins update last activity, this is to keep session active
        now = timezone.now()
        delta = datetime.timedelta(Settings.SELLER_SESSION_UPDATE_TIME)


        lastActivity = request.session.get('lastActivityTime', False)
        if not lastActivity:
            # looks like the session is broken
            # TODO clear the session
            logger.debug('Broken session')
            pass
        
        if lastActivity + delta < now:
            request.session['lastActivityTime'] = timezone.now()       
        

        return True
    # remove bad sessions - this fixed in the later version. Happy !
    request.COOKIES = {}
    request.session.flush()

    return False

def delete_seller_session(request):
    '''
        assumes session is valid
    '''
    request.session.flush()



#http://stackoverflow.com/questions/238260/how-to-calculate-the-bounding-box-for-a-given-lat-lng-location
# degrees to radians
def deg2rad(degrees):
    return math.pi*degrees/180.0
# radians to degrees
def rad2deg(radians):
    return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000*halfSideInKm

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    latMin = lat - halfSide/radius
    latMax = lat + halfSide/radius
    lonMin = lon - halfSide/pradius
    lonMax = lon + halfSide/pradius

    return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))
 
def latLonRoundDown(latitude, longitude):
    
    latitude = int(latitude * Constants.latLongMultiplyer)
    latitude = latitude - (latitude % Constants.latLongModulo)
    
    longitude = int(longitude * Constants.latLongMultiplyer)
    longitude = longitude - (longitude % Constants.latLongModulo)

    return (latitude, longitude)

def latLonRoundUp(latitude, longitude):
    latitude = int(latitude * Constants.latLongMultiplyer)
    latitude = latitude + (latitude % Constants.latLongModulo)

    longitude = int(longitude * Constants.latLongMultiplyer)
    longitude = longitude + (longitude % Constants.latLongModulo)

    return (latitude, longitude)



def overlapping_tiles(latitude, longitude, squareSize=15):
    latMin, lonMin, latMax, lonMax = boundingBox(latitude, longitude, squareSize/2)

    latMin, lonMin = latLonRoundDown(latMin, lonMin)

    latMax, lonMax = latLonRoundUp(latMax, lonMax)

    
    tiles = []

    # sweep the grid to create all tiles
    for lat in range(latMin, latMax, Constants.latLongModulo):
        for lon in range(lonMin, lonMax, Constants.latLongModulo):
            tiles.append('{0:06}_{1:06}'.format(lat, lon))

    return tiles



def rankeSellers(sellers):
    return sellers


def validateMessage(message):
    return True


def shortenMessage(message):
    return message[:100]


def jsonizeDjangoObject(obj):
    return serializers.serialize('json', obj)
