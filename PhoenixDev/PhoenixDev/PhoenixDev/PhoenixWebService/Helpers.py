import json



class StatusCodes():
    # have two members per code
    Success = 0
    InvalidPhoneNum = 1
    


class StatusMessage():
    statusMessages = {}
    statusMessages[StatusCodes.InvalidPhoneNum] = 'Invalid phone number'
    statusMessages[StatusCodes.Success] = 'Success'

    



def create_json_output(statusCode, data):

    output = {}

    if statusCode not in StatusMessage.statusMessages:
        raise NotImplementedError
    
    output['status'] = { 'statusCode' : statusCode, 'statusMessage' : StatusMessage.statusMessages[statusCode] }
    output['data'] = data

    return json.dumps(output)

