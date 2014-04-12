from django.shortcuts import render
from django.http import HttpResponse
import json

import os, sys
lib_path = os.path.abspath('/home/richard/website/mlproject/MSDChallenge-project-Spring2014/src')
sys.path.append(lib_path)

from CollaborativeUsersPredictor import CollaborativeUsersPredictor

predictor = CollaborativeUsersPredictor()
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def user_page(request, user_id):

    predictions = predictor.predict(predictor.user2songs.values()[int(user_id)])
    return HttpResponse(json.dumps(map(lambda x: int(x), predictions)))
