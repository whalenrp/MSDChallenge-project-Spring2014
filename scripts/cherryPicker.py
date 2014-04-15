# Cherry Picker - grabs:
#	artist_name, title, filename, songID, and key
# from msd h5 files

# referencing: http://stackoverflow.com/questions/2212643/python-recursive-folder-read
# and		 : http://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac

import os
import sys
import hdf5_functions


savePath = "C:\\Users\\Aluminum\\Desktop\\"
outfilePath = os.path.join(savePath,"test.txt")
songIdDict = {"init":"init"}
keyDict = {"init":"init"}

# process taste_profile_song_to_tracks to map filename -> songID
with open ("taste_profile_song_to_tracks.txt",'r') as r:
	for line in r:
		splitLine = line.split(' ')
		for fileName in splitLine: # handles multiple filenames -> 1 songID
			if splitLine.index(fileName) != 0:
				songIdDict["" + fileName.rstrip()] = "" + splitLine[0].rstrip()

# process kaggle_songs to map songID -> key
with open("kaggle_songs.txt",'r') as r:
	for line in r:
		songID, key = line.split(' ')[:2]
		keyDict["" + songID.rstrip()] = "" + key.rstrip()

# change rootdir according to where the script is
rootdir = "C:\\Users\\Aluminum\\Documents\\Academics\\2014Spring\\CS292\\FinalProject\\MSDChallenge-project-Spring2014\\scripts\\HoldsA\\"
for root, subFolders, files in os.walk(rootdir):
	with open(outfilePath, 'a') as fileOut:
			
		for fileName in files:
			trackFileName = os.path.splitext(fileName)[0]
			songID = songIdDict[trackFileName]
			key = keyDict[songID]
			
			artist_name = hdf5_functions.get_artist_name(h5)
			title = hdf5_functions.get_title(h5)
			
			
			fileOut.write(key + " " + trackFileName + " " + songID + "\n")
			