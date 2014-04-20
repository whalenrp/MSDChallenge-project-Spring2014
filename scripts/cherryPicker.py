# Cherry Picker - grabs:
#	artist_name, title, filename, songID, and key
# from msd h5 files

# requires both taste_profile_song_to_tracks.txt and 
#				kaggle_songs.txt
# to be in the same directory as this script to run correctly

# referencing: http://stackoverflow.com/questions/2212643/python-recursive-folder-read
# and		 : http://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac

import os
import sys
import hdf5_functions


savePath = "C:\\Users\\meow\\Downloads\\"
outfilePath = os.path.join(savePath,"test.txt")
songIdDict = {"init":"init"}
keyDict = {"init":"init"}

# process taste_profile_song_to_tracks to map filename -> songID
with open ("E:\\Kaggle\\taste_profile_song_to_tracks.txt",'r') as r:
	for line in r:
		splitLine = line.split('\t')
		for fileName in splitLine[1:]: # handles multiple filenames -> 1 songID
			songIdDict[str(fileName.rstrip())] = str(splitLine[0].rstrip())

# process kaggle_songs to map songID -> key
with open("E:\\Kaggle\\kaggle_songs.txt",'r') as r:
	for line in r:
		songID, key = line.split(' ')[:2]
		keyDict["" + songID.rstrip()] = "" + key.rstrip()

# change rootdir according to where the source h5 files are
rootdir = "E:\\A"
fileOut = open(outfilePath, 'w')
for root, subFolders, files in os.walk(rootdir):
			
		for fileName in files:
			if fileName.lower().endswith(".h5"):
				trackFileName = os.path.splitext(fileName)[0]
				if trackFileName in songIdDict:
					songID = songIdDict[trackFileName]
					key = keyDict[songID]

					# I am continuing under the assumption this is correct
					h5 = hdf5_functions.open_h5_file_read(os.path.join(root, fileName))
					artistName = hdf5_functions.get_artist_name(h5)
					title = hdf5_functions.get_title(h5)
					h5.close()
					
					fileOut.write(key + "\t" + trackFileName + "\t" + songID + "\t" + artistName + "\t" + title + "\n")
fileOut.close()