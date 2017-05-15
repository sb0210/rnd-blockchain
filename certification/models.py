from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    private_key = models.CharField(max_length=3000)
    public_key = models.CharField(max_length=3000)
    def __str__(self):             
        return self.user.username


class Validator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    blocks = models.ManyToManyField('Block', blank=True)
    chain_length = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return self.name



# Create your models here.
class Block(models.Model):
    id = models.AutoField(primary_key=True)
    block_number = models.IntegerField()
    validators = models.ForeignKey(Validator)
    nonce = models.IntegerField()
    student = models.ForeignKey(Student)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    file = models.FileField(upload_to='documents/')
    file_hash = models.CharField(max_length=64)
    signature1 = models.CharField(max_length=64)
    signature2 = models.CharField(max_length=64)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.block_number)



