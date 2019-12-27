from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import json

def index(request):
    return render(request, 'mySite/index.html')