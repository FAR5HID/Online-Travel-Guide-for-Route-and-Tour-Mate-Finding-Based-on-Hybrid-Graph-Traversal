from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class Spots(models.Model):
    
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    rating = models.IntegerField()
    district = models.CharField(max_length=100)
    category = ArrayField(models.CharField(max_length=100), blank=True)
    
    def __str__(self):
        return self.name
    
class Edges(models.Model):
    n1 = models.CharField(max_length=100)
    n2 = models.CharField(max_length=100)
    minute = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return self.n1 + '-' + self.n2