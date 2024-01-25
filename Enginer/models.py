from django.db import models


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    salary = models.FloatField()
    city = models.CharField(max_length=100)
    published_date = models.DateField()
