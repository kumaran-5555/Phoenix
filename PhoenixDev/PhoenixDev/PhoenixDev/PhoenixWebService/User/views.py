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



def signup(request):
    if request.method != 'POST':
        return HttpResponse('NOT POST')

    phoneNumber =  request.POST.get('phoneNumber', False)

    # validation
    if not phoneNumber or len(phoneNumber) != 10 or not phoneNumber.isdigit():
        return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.InvalidPhoneNum, phoneNumber))

    now = timezone.now()
    delta = datetime.timedelta(seconds=Settings.OTP_VALID_TIME_SECONDS)

    otpValue = '55555'
    Helpers.logger.debug(otpValue)


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
        else:
            # already exists and valid no need to update
            otpValue = row.otpValue
            pass

    except User.models.OTPMappings.DoesNotExist:
        # create new 
        User.models.OTPMappings.objects.create(phoneNumber = phoneNumber, otpValue=otpValue, expiaryDate=now + delta)

    # send otp
    # TODO - for now use simple return, we will use SMS api

    return HttpResponse(Helpers.create_json_output(Helpers.StatusCodes.Success, {'otpValue': otpValue }))
  





def signup_resendotp(request):
    if request.method != 'POST':
        return HttpResponseNotFound()


def signup_otpvalidation(request):
    if request.method != 'POST':
        return HttpResponse('NOT POST')
    
    phoneNumber =  request.POST['phoneNumber']
    otpValue = request.POST['otpValue']

    
