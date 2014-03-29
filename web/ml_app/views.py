from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def user_page(request, user_id):
    return HttpResponse("Hello, " + user_id + "!")
