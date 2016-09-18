from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validateReg(self, request):
        errors = self.validate_inputs(request)
        if len(errors) > 0:
            return (False, errors)
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        user = self.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash, birthdate=request.POST['birthdate'])
        return (True, user)

    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.password.encode()) == user.password:
                return (True, user)
        except ObjectDoesNotExist:
            pass
        return (False, ["Email/password don't match."])

    def validate_inputs(self, request):
        errors = []
        if len(request.POST['name']) < 2 or len(request.POST['alias']) < 2:
            errors.append("Please include a name and alias longer than two characters.")
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Please include a valid email.")
        if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['confirm_pw']:
            errors.append("Passwords must match and be at least 8 characters.")
        if len(request.POST['birthdate']) < 8:
            errors.append("Please provide a date of birth.")
        if len(request.POST['birthdate']) >= 8:
            s = request.POST['birthdate']
            f = "%Y-%m-%d"
            date = datetime.datetime.strptime(s, f)
            if date > datetime.datetime.now():
                errors.append("Fetuses and time travelers cannot register on this site!")
        try:
            if User.objects.get(email=request.POST['email']):
                errors.append("That email is already associated with an account")
        except ObjectDoesNotExist:
            pass
        return errors


class PokeManager(models.Manager):
    def poke(self, user_id, poked_id):
        user = User.objects.get(id = user_id)
        poked_user = User.objects.get(id = poked_id)
        self.create(pokedUser=poked_user, UserWhoPoked=user)
        return (True)


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Poke(models.Model):
    pokedUser = models.ForeignKey(User, related_name='poked_user')
    UserWhoPoked = models.ForeignKey(User, related_name='user_who_poked')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PokeManager()
