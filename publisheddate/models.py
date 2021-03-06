from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Authors(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Book(models.Model):
    authors = models.ForeignKey(Authors, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    book_publish_date = models.CharField(max_length=20, null=True)
    #categories = models.CharField(max_length=200, null=True)
    categories = models.JSONField()
    average_rating = models.CharField(max_length=5, null=True)
    ratings_count = models.CharField(max_length=5, null=True)
    thumbnail = models.TextField()

    def __str__(self):
        return self.title
