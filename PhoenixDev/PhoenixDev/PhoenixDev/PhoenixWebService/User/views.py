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


def signup(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    phoneNumber =  request.POST.get('phoneNumber', False)

    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
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

    
    try:
        row = User.models.OTPMappings.objects.get(phoneNumber=phoneNumber)
        # check if opt is correct and valid
        if row.expiaryDate < now and row.otpValue == otpValue:
            Helpers.logger.debug('Otp exists and valid {0}'.format(otpValue))
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, otpValue))
        else:
            # already exists and valid no need to update
            Helpers.logger.debug('Otp exists, but invalid {0}'.format(otpValue))  
            return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, {'otpValue': otpValue }))          


    except User.models.OTPMappings.DoesNotExist:
        # create new 
        Helpers.logger.debug('Otp doesnot exists {0}'.format(otpValue))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.OtpValidationFailed, otpValue))


def signup_password(request):
    if request.method != 'POST':
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.NotPostRequest, ''))

    password = request.POST.get('password', False)
    phoneNumber =  request.POST.get('phoneNumber', False)

    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        Helpers.logger.debug('Invalid phoneNumber {0}'.format(phoneNumber))
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))

    if not password or len(password) > 15 or not re.match(Settings.PASSWORD_REGEX_PATTERN, password):
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPassword, ''))

    # create sha512
    hashObj = hashlib.sha512()
    hashObj.update(password)
    hashObj.update(phoneNumber)
    hashObj.update(Settings.SECRET_KEY)
    hash = hashObj.hexdigest()

    row = User.models.Users(userPrimaryPhone=phoneNumber, userPasswordHash=hash)

    row.save()

    Helpers.logger.debug('User added successfully with phoneNumber {0}'.format(phoneNumber))
    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, 'added'))   




