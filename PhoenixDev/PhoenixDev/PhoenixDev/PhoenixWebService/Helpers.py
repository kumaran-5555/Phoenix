import json
import logging

import Settings



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



    



def create_json_output(statusCode, data):

    output = {}

    if statusCode not in StatusMessage.statusMessages:
        raise NotImplementedError
    
    output['status'] = { 'statusCode' : statusCode, 'statusMessage' : StatusMessage.statusMessages[statusCode] }
    output['data'] = data

    return json.dumps(output)

