# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound

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
        row = User.models.Users.objects.get(userPrimaryPhone=phoneNumber)        
        pass

    except User.models.Users.MultipleObjectsReturned:
        # Alert: shouldn't come here
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))
    except (User.models.Users.DoesNotExist):
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
        row = User.models.OTPMappings.objects.get(phoneNumber=phoneNumber)
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
            

    except User.models.OTPMappings.DoesNotExist:
        # create new 
        User.models.OTPMappings.objects.create(phoneNumber = phoneNumber, otpValue=otpValue, expiaryDate=now + delta)
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
    try:
        row = User.models.Users.objects.get(userPrimaryPhone=phoneNumber)
        # get is successful
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.PhoneNumAlreadyExists, phoneNumber))
    except User.models.Users.MultipleObjectsReturned:
        # Alert: shouldn't come here
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.PhoneNumAlreadyExists, phoneNumber))
    except (User.models.Users.DoesNotExist):
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
        row = User.models.OTPMappings.objects.get(phoneNumber=phoneNumber)
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
            

    except User.models.OTPMappings.DoesNotExist:
        # create new 
        User.models.OTPMappings.objects.create(phoneNumber = phoneNumber, otpValue=otpValue, expiaryDate=now + delta)
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
        row = User.models.OTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if opt is correct and valid
        if row.expiaryDate > now and row.otpValue == otpValue:
            Helpers.logger.debug('Otp exists and valid {0}'.format(otpValue))
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, otpValue))
        else:
            # already exists and valid no need to update
            Helpers.logger.debug('Otp exists, but invalid {0} expirary {1} now {2}'.format(otpValue, row.expiaryDate, now))  
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, {'otpValue': otpValue}))          


    except User.models.OTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))


def signup_password(request):
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
        row = User.models.OTPMappings.objects.get(phoneNumber=phoneNumber)
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


    except User.models.OTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))



    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()

    row, isCreated = User.models.Users.objects.get_or_create(userPrimaryPhone=phoneNumber)
    if not isCreated:
        # phonenum already exists
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))


    # adding new user password
    row.userPasswordHash=hash
    row.save()

    Helpers.logger.debug('User added successfully with phoneNumber {0}'.format(phoneNumber))
    response = HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'added'))   

    Helpers.create_user_session(request, phoneNumber, row.id)

    return response



def reset_password(request):
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
        row = User.models.OTPMappings.objects.get(phoneNumber=phoneNumber)
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


    except User.models.OTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))



    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()

    try:
        row = User.models.Users.objects.get(userPrimaryPhone=phoneNumber)

    except User.models.User.DoesNotExist:
        # phonenum doesn't exists, we want phonenumber to be present
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))


    # resetting password
    row.userPasswordHash=hash
    row.save()

    Helpers.logger.debug('Seller password reset success with phoneNumber {0}'.format(phoneNumber))
    response = HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'reset'))   

    Helpers.create_user_session(request, phoneNumber, row.id)

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


    now = timezone.now()

    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()

    try:
        row = User.models.Users.objects.get(userPrimaryPhone=phoneNumber, userPasswordHash=hash)
        # user name is valid

    except User.models.Users.DoesNotExist:

        Helpers.logger.debug('Invalid username password {0} {1}'.format(phoneNumber, password))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUsernamePassword, ''))

    # create session here 
    response = HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, ''))
    
    Helpers.create_user_session(request, phoneNumber, row.id)

    return response


def logout(request):
    if request.method != 'GET':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotGetRequest, ''))

    if not Helpers.validate_user_session(request):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidUserSession, ''))

    Helpers.delete_user_session(request)

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'logged out'))


