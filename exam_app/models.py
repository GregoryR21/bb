from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] =  "Invalid email address"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Passwords don't match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login'] =  "Invalid Email/Password"
        if len(postData['login_pw']) < 8:
            errors["login"] = "Invalid Email/Password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self): 
        return f"<ID: {self.id} First Name: {self.first_name} Last Name: {self.last_name} Email: {self.email}>"

class ThoughtManager(models.Manager):
    def thought_validator(self, postData):
        errors = {}
        if len(postData['thought']) < 5:
            errors["thought"] = "Thought should be at least 5 characters"
        return errors

class Thought(models.Model):
    thought = models.TextField()
    user = models.ForeignKey(User, related_name="thoughts", on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ThoughtManager()
    def __repr__(self): 
        return f"<ID: {self.id} Thought: {self.thought}>"