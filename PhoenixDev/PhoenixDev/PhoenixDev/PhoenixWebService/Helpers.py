import json
import logging

import Settings

from django.utils import timezone
import datetime

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





    



def create_json_output(statusCode, data):

    output = {}

    if statusCode not in StatusMessage.statusMessages:
        raise NotImplementedError
    
    output['status'] = { 'statusCode' : statusCode, 'statusMessage' : StatusMessage.statusMessages[statusCode] }
    output['data'] = data

    return json.dumps(output)




def create_user_session(request, phoneNumber):
    '''
        creates session in request
    '''

    # set session 
    request.session['phoneNumber'] = phoneNumber
    request.session['loggedInTime'] = timezone.now()
    request.session['lastActivityTime'] = timezone.now()
    request.session['type'] = Settings.USER_TYPE
    

     


def validate_user_session(request):
    '''
        validates session and updates timestamps
        if required

        returns boolean
    '''
    
    if request.session.get('phoneNumber', False):
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
    
    return False

def delete_user_session(request):
    '''
        assumes session is valid
    '''
    request.session.flush()





