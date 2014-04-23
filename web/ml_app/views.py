from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
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

def users_json(request, user_id):
	if request.GET.get('user',''):
		user_id = request.GET['user']
	predictions = predictor.predict(predictor.user2songs.values()[int(user_id)])
	history = predictor.user2songs.values()[int(user_id)]
	client = MongoClient()
	db = client['test']
	collection = db.msdinfo
	history_list = []
	for song in history:
		res = collection.find_one({"id":str(song)})
		if res:
			history_list.append(res)
	prediction_list = []
	for song in predictions:
		res = collection.find_one({"id":str(song)})
		if res:
			prediction_list.append(res)
	return render_to_response('index.html', {'history':history_list, 'predictions':prediction_list, 'user_id': user_id}, context_instance=RequestContext(request))
	

def song_info(request, song_id):
	client = MongoClient()
	db = client['test']
	collection = db.msdinfo
	query_result = collection.find_one({"id":str(song_id)})
	return HttpResponse(dumps(query_result))
	#return HttpResponse("hi")
