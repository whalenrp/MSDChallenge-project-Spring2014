#!/usr/bin/env python

import math
# First find max playcount
# use max playcount to normalize data
# Read in users
# for each user, add their corresponding song entries

songMapping = dict();
with open('kaggle_songs.txt', 'r') as f:
	for line in f:
		song,index = line.strip().split()
		songMapping[song] = int(index)
	pass
pass

userFile = open('kaggle_users.txt', 'r')
userPlaysFile = open('kaggle_visible_evaluation_triplets.txt','r')
dataOutputFile = open('sanitized_data.txt','w')

userIndex = 1
for line in userFile:
	curUser = line.strip()
	dataOutputFile.write(curUser)
	#dataOutputFile.write(str(userIndex))
	userIndex += 1
	playcountUser,song,count = userPlaysFile.readline().strip().split()
	while curUser == playcountUser:
		dataOutputFile.write(" " + str(songMapping[song]) + ":1")
		line = userPlaysFile.readline()
		if line == "" : break
		playcountUser,song,count = line.strip().split()
	pass
	dataOutputFile.write('\n')
pass

dataOutputFile.close();
userPlaysFile.close();
userFile.close();

