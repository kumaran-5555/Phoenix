# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.core import validators


import json

from PhoenixDev.PhoenixWebService import *
from PhoenixDev.PhoenixWebService import Helpers
from PhoenixDev.PhoenixWebService import Settings


from django.shortcuts import render_to_response
from django.core.exceptions import *

import random
from django.utils import timezone
import datetime
import random
import re
import hashlib


def forgot_password(request):
    '''
        same as signup, but the phonenumber must be in users table.
        after this follow, otpvalidation, and reset password
    '''

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    phoneNumber =  request.POST.get('phoneNumber', False)

    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))
    
    # check whether the phonenumber is already signed-up
    try:
        row = Seller.models.Sellers.objects.get(sellerPrimaryPhone=phoneNumber)        
        pass

    except Seller.models.Sellers.MultipleObjectsReturned:
        # Alert: shouldn't come here
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))
    except (Seller.models.Sellers.DoesNotExist):
        # Alert: shouldn't come here
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))
        
    
    now = timezone.now()
    delta = datetime.timedelta(seconds=Settings.OTP_VALID_TIME_SECONDS)

    # get random otp

    otpValue = str(random.randint(10000, 99999))
    Helpers.logger.debug('Generated optValue {0}'.format(otpValue))


    # we maintain only single row per phonenumber - invariant
    # check if otp already exist and valid, reuse
    # already exists but invalid, create new 
    # doesn't exists, create new
    try:
        row = Seller.models.SellerOTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if the found has expired
        if row.expiaryDate < now:
            # update new
            row.expiaryDate = now + delta
            row.otpValue = otpValue
            row.save()
            Helpers.logger.debug('Otp exists but expired, updating to new optValue {0}'.format(otpValue))
        else:
            # already exists and valid no need to update
            otpValue = row.otpValue
            Helpers.logger.debug('Otp exists, not expired, reusing optValue {0}'.format(otpValue))
            

    except Seller.models.SellerOTPMappings.DoesNotExist:
        # create new 
        Seller.models.SellerOTPMappings.objects.create(phoneNumber = phoneNumber, otpValue=otpValue, expiaryDate=now + delta)
        Helpers.logger.debug('Otp doesnot exists, using optValue {0}'.format(otpValue))

    # send otp
    # TODO - for now use simple return, we will use SMS api

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'otpValue': otpValue }))

def signup(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    phoneNumber =  request.POST.get('phoneNumber', False)

    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))
    
    # check whether the phonenumber is already signed-up
    # TODO - can a phonenumber be seller as well as user ??
    try:
        row = Seller.models.Sellers.objects.get(sellerPrimaryPhone=phoneNumber)
        # get is successful
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.PhoneNumAlreadyExists, phoneNumber))
    except Seller.models.Sellers.MultipleObjectsReturned:
        # Alert: shouldn't come here
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.PhoneNumAlreadyExists, phoneNumber))
    except (Seller.models.Sellers.DoesNotExist):
        pass
    
    now = timezone.now()
    delta = datetime.timedelta(seconds=Settings.OTP_VALID_TIME_SECONDS)

    # get random otp

    otpValue = str(random.randint(10000, 99999))
    Helpers.logger.debug('Generated optValue {0}'.format(otpValue))


    # we maintain only single row per phonenumber - invariant
    # check if otp already exist and valid, reuse
    # already exists but invalid, create new 
    # doesn't exists, create new
    try:
        row = Seller.models.SellerOTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if the found has expired
        if row.expiaryDate < now:
            # update new
            row.expiaryDate = now + delta
            row.otpValue = otpValue
            row.save()
            Helpers.logger.debug('Otp exists but expired, updating to new optValue {0}'.format(otpValue))
        else:
            # already exists and valid no need to update
            otpValue = row.otpValue
            Helpers.logger.debug('Otp exists, not expired, reusing optValue {0}'.format(otpValue))
            

    except Seller.models.SellerOTPMappings.DoesNotExist:
        # create new 
        Seller.models.SellerOTPMappings.objects.create(phoneNumber = phoneNumber, otpValue=otpValue, expiaryDate=now + delta)
        Helpers.logger.debug('Otp doesnot exists, using optValue {0}'.format(otpValue))

    # send otp
    # TODO - for now use simple return, we will use SMS api

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'otpValue': otpValue }))
  

def signup_resendotp(request):
    if request.method != 'POST':
        return HttpResponseNotFound()


def signup_optvalidation(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))
    
    phoneNumber =  request.POST.get('phoneNumber', False)
    otpValue = request.POST.get('otpValue', False)

    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))

    if not  otpValue or len(otpValue) != 5 or not otpValue.isdigit():
        Helpers.logger.debug('Invalid otpValue {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOtpValue, otpValue))

    now = timezone.now()
    
    try:
        row = Seller.models.SellerOTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if opt is correct and valid
        if row.expiaryDate > now and row.otpValue == otpValue:
            Helpers.logger.debug('Otp exists and valid {0}'.format(otpValue))
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, otpValue))
        else:
            # already exists and valid no need to update
            Helpers.logger.debug('Otp exists, but invalid {0} expirary {1} now {2}'.format(otpValue, row.expiaryDate, now))  
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, {'otpValue': otpValue}))          


    except Seller.models.SellerOTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))


def signup_password(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    password = request.POST.get('password', False)
    phoneNumber =  request.POST.get('phoneNumber', False)
    otpValue = request.POST.get('otpValue', False)
    sellerName = request.POST.get('sellerName', False)
    cityName = request.POST.get('cityName', False)
    address = request.POST.get('address', False)
    # TODO - do we need secondary phonenumber, we need validation of 
    # secondary phonenumber before using it
    #secondaryPhone = request.POST.get('secondaryPhoneNumber', False)
    latitude = request.POST.get('latitude', False)
    longitude = request.POST.get('longitude', False)
    mailId = request.POST.get('mailId', False)
    website = request.POST.get('website', False)
    description = request.POST.get('description', False)
    appId = request.POST.get('appId', False)



    # we share the otp with user as secret, only the users
    # who have correct otp and phonenumber match and valid
    # opt are allowed to add password



    # validation
    if not  otpValue or len(otpValue) != 5 or not otpValue.isdigit():
        Helpers.logger.debug('Invalid otpValue {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOtpValue, otpValue))


    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))

    if not password or len(password) > 15 or not re.match(Settings.PASSWORD_REGEX_PATTERN, password):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPassword, ''))
    now = timezone.now()

    # validdate otp
    try:
        otpRow = Seller.models.SellerOTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if opt is correct and valid
        if otpRow.expiaryDate > now and otpRow.otpValue == otpValue:
            # rest is handled below
            pass             
            
        else:
            # already exists and valid no need to update
            Helpers.logger.debug('Otp exists, but invalid {0}'.format(otpValue))  
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, {'otpValue': otpValue }))          


    except Seller.models.SellerOTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))

    # valid otp mapping exists
    Helpers.logger.debug('Otp exists and valid {0}'.format(otpValue))

    # validate other params and create seller profile if validation passes
    # keep otp alive till we validate all params

    if not sellerName or len(sellerName) > 100 or not re.match(Settings.SELLER_NAME_REGEX_PATTERN, sellerName):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerName, sellerName))


    if not cityName or len(cityName) > 50 or not cityName.isalpha():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidCityName, cityName))


    #TODO - address validation ?
    if not address or len(address) > 300:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidAddress, address))

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

    # mail is optional, so validate only if provided

    if mailId:
        if not re.match(Settings.EMAIL_REGEX_PATTERN, mailId):
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidMailId, mailId))
    else:
        mailId = ''


    # website is optional and validate only if provided
    
    

    if website:
        urlValidator = validators.URLValidator()

        try:
            urlValidator(website)
        except ValidationError:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidWebsite, website))
    else:
        website = ''
        


    # TODO - description validation ?
    # description is optional
    
    if description:
        if len(description) > 1024:
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidDescription, description))
    else:
        description = ''
    
     
    if not appId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidAppId, appId))






    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()
    
    row = None
    try:
        row = Seller.models.Sellers.objects.get(sellerPrimaryPhone=phoneNumber)

    except Seller.models.Sellers.DoesNotExist:
        pass



    # row already exists 
    if row:
        # phonenum already exists
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.PhoneNumAlreadyExists, phoneNumber))

    Helpers.logger.debug('New seller profile phone:{} name:{} city:{} ,\
            address:{} latitude:{} longitude:{} mailId:{} website:{} desc:{}'.format(\
                phoneNumber, sellerName, cityName, address, latitude, longitude, mailId, website, description))

    row = Seller.models.Sellers()

    # adding new user password 
    row.sellerPrimaryPhone = phoneNumber
    row.sellerName = sellerName
    row.sellerCityName = cityName
    row.sellerAddress = address
    row.sellerLatitude = latitude
    row.sellerLongitude = longitude
    row.sellerMailId = mailId
    row.sellerWebsite = website
    row.sellerDescription= description

    row.sellerPasswordHash=hash
    row.sellerAppId = appId

    row.save()

    Helpers.logger.debug('seller added successfully with phoneNumber {0}'.format(phoneNumber))
    response = HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'added'))   

    Helpers.create_seller_session(request, phoneNumber, row.id)

    # make the otp expired, the otp is job is done
    
    otpRow.expiaryDate = now
    otpRow.save()

    return response

def reset_password(request):
    '''
        profile update
    '''

    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    password = request.POST.get('password', False)
    phoneNumber =  request.POST.get('phoneNumber', False)
    otpValue = request.POST.get('otpValue', False)

    # we share the otp with user as secret, only the users
    # who have correct otp and phonenumber match and valid
    # opt are allowed to add password



    # validation
    if not  otpValue or len(otpValue) != 5 or not otpValue.isdigit():
        Helpers.logger.debug('Invalid otpValue {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidOtpValue, otpValue))


    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))

    if not password or len(password) > 15 or not re.match(Settings.PASSWORD_REGEX_PATTERN, password):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPassword, ''))
    now = timezone.now()

    # validdate otp
    try:
        row = Seller.models.SellerOTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if opt is correct and valid
        if row.expiaryDate > now and row.otpValue == otpValue:
            # valid otp mapping exists
            Helpers.logger.debug('Otp exists and valid {0}'.format(otpValue))
            # make the otp expired, the otp is job is done
            row.expiaryDate = now
            row.save()
            
        else:
            # already exists and valid no need to update
            Helpers.logger.debug('Otp exists, but invalid {0}'.format(otpValue))  
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, {'otpValue': otpValue }))          


    except Seller.models.SellerOTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))

    appId = request.POST.get('appId', False)

    if not appId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidAppId, appId))

    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()

    try:
        row = Seller.models.Sellers.objects.get(sellerPrimaryPhone=phoneNumber)

    except Seller.models.Sellers.DoesNotExist:
        # phonenum doesn't exists, we want phonenumber to be present
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))


    # resetting password
    row.sellerPasswordHash=hash
    row.sellerAppId = appId
    row.save()

    Helpers.logger.debug('Seller password reset success with phoneNumber {0}'.format(phoneNumber))
    response = HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'reset'))   

    Helpers.create_seller_session(request, phoneNumber, row.id)

    return response

def login(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    password = request.POST.get('password', False)
    phoneNumber =  request.POST.get('phoneNumber', False)

    # we share the otp with user as secret, only the users
    # who have correct otp and phonenumber match and valid
    # opt are allowed to add password
    
    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))

    if not password or len(password) > 15 or not re.match(Settings.PASSWORD_REGEX_PATTERN, password):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPassword, ''))

    appId = request.POST.get('appId', False)

    if not appId:
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidAppId, appId))

    now = timezone.now()

    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()

    try:
        row = Seller.models.Sellers.objects.get(sellerPrimaryPhone=phoneNumber, sellerPasswordHash=hash)
        # seller name is valid
        row.sellerAppId = appId
        row.save()


    except Seller.models.Sellers.DoesNotExist:

        Helpers.logger.debug('Invalid seller name or password {0} {1}'.format(phoneNumber, password))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUsernamePassword, ''))

    # create session here 
    response = HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, ''))
    
    Helpers.create_seller_session(request, phoneNumber, row.id)

    return response


def logout(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))

    if not Helpers.validate_seller_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidSellerSession, ''))

    Helpers.delete_seller_session(request)

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'logged out'))


