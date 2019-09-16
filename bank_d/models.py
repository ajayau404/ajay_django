from django.conf import settings
from django.db import models
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

class Banks(models.Model):
    name 		= models.CharField(max_length=49)
    bankid 		= models.BigIntegerField(primary_key=True)
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "{}".format(self.name)



class Branches(models.Model):
    ifsc 		= models.CharField(max_length=11, primary_key=True)
    bank 		= models.ForeignKey(Banks, on_delete=models.CASCADE)
    branch 		= models.CharField(max_length=74) 
    address 	= models.TextField()
    city 		= models.CharField(max_length=80)
    district 	= models.CharField(max_length=50)
    state 		= models.CharField(max_length=26)

    class Meta:
        ordering = ('branch',)
        verbose_name = 'Branch'
        verbose_name_plural = 'Branch'
    
    def __str__(self):
        return "{} - {} - {}".format(self.branch, self.city, self.bank)