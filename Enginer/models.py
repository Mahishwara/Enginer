from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=100)


class Salary(models.Model):
    year = models.IntegerField()
    value = models.FloatField()
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    salary = models.FloatField()
    region = models.CharField(max_length=100)
    published_date = models.DateField()
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
