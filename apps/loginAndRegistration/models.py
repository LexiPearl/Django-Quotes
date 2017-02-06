from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+([a-zA-Z]+)*$')

class UserManager(models.Manager):
    def UserValidator(self, postData):
        flag=False
        errors=[]
        if len(postData['name']) < 3:
            errors.append("Name must be at least 3 characters!")
            flag=True
        elif not NAME_REGEX.match(postData['name']):
            errors.append("Invalid name!")
            flag=True
        if len(postData['alias']) <3:
            flag=True
            errors.append("Alias must be at least 3 characters!")
        if len(postData['email'])<3:
            flag=True
            errors.append("Email must be at least 3 characters!")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email!")
            flag=True
        if len(postData['password'])<8:
            flag=True
            errors.append("Password length is invalid")
        if len(postData['password_confirmation']) < 1:
            errors.append("Confirm password cannot be empty!")
            flag=True
        if postData['password_confirmation'] != postData['password']:
            flag=True
            errors.append("Passwords do not match!")
        if not flag:
            pwhash= bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt())
            User.objects.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                password= pwhash,
                birthday=postData['birthday'])
            user = User.objects.last()
            return (flag, user)
        return (flag, errors)
    def userLogin(self, postData):
        login= User.objects.filter(email=postData['email'])
        if len(login)<1:
            return (False, "User does not exist in database")
        else:
            user= User.objects.get(email=postData['email'])
            password= postData['password'].encode()
            hashed=user.password.encode()
            if bcrypt.hashpw(password, hashed )== hashed and user:
                return (True, user)
            else:
                return (False, "Email and password do not match")

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    birthday= models.DateTimeField(max_length=40, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()
