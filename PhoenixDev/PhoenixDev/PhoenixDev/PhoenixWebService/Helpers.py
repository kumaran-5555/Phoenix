import json
import logging
import re

import Settings

from django.utils import timezone
import datetime
from PhoenixDev.PhoenixWebService import *


logger = logging.getLogger(Settings.LOGGERNAME)



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
            pass
        
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