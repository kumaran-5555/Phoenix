from django.db import models


class Users(models.Model):
    '''
        primary table to store user related information
    '''
    userName = models.CharField(max_length=100)
    userPrimaryPhone = models.CharField(max_length=11)
    userMailId = models.CharField(max_length=100)
    # For completion sake, these fields can be optional for user.
    userCityName = models.CharField(max_length=50)
    userAddress = models.CharField(max_length=300)
    # sha512
    userPasswordHash = models.CharField(max_length=512)
    userSignupTime = models.DateTimeField(auto_now_add=True)
