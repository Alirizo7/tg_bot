from django.shortcuts import render

# Create your views here.
from .helpers import *
from django.http import JsonResponse


def home(request):
    return JsonResponse({'status': 200})
