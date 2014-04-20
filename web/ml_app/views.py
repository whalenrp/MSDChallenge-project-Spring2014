from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from bson.json_util import dumps
import json

import os, sys
lib_path = os.path.abspath('/home/ubuntu/MSDChallenge-project-Spring2014/src')
sys.path.append(lib_path)

from CollaborativeUsersPredictor import CollaborativeUsersPredictor

predictor = CollaborativeUsersPredictor()
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def user_info(request, user_id):
    predictions = predictor.predict(predictor.user2songs.values()[int(user_id)])
    return HttpResponse(json.dumps({"listening_history":predictor.user2songs.values()[int(user_id)],"predictions":map(lambda x: int(x), predictions)}))

def song_info(request, song_id):
    client = MongoClient()
    db = client['test']
    collection = db.msdinfo
    query_result = collection.find_one({"id":str(song_id)})
    return HttpResponse(dumps(query_result))
    #return HttpResponse("hi")
