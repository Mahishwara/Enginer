import requests
from django.shortcuts import render
from Enginer.models import Vacancy
import Enginer.models as models
from datetime import datetime, timedelta



def home(request):
    return render(request, 'home.html')


def demand(request):
    return render(request, 'demand.html')


def geography(request):
    return render(request, 'geography.html')


def skills(request):
    return render(request, 'skills.html')


def latest_vacancies(request):
    return render(request, 'last_vac.html')
