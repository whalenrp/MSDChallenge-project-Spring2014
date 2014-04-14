# Cherry Picker - grabs:
#	artist_name, title, filename, songID, and key
# from msd h5 files

# referencing: http://stackoverflow.com/questions/2212643/python-recursive-folder-read
import os
import sys
#import hdf5_functions

#rootdir = sys.argv[1]

# process taste_profile_song_to_tracks to map filename -> songID

# process kaggle_songs 				   to map songID -> key

# 1) determine current file name
# 2) look up songID in taste_profile_song_to_tracks
# 3) look up key using songID in kaggle_songs
# 4) pull artist_name from h5
# 5) pull song title from h5

# store data in a written format
# txt file --> fname songID key artist_name song_title

#for root, subFolders, files in os.walk(rootdir):
outfileName = "C:\Users\Aluminum\Desktop\test.txt"
with open("test.txt", 'w') as fileOut:
	#for fileName in files:
	#	filePath = os.path.join(root,fileName)
		
	#	with open(filePath, 'r') as f:
	#		toWrite = f.read()
	#		fileOut.write("The file %s contains %s" % (filePath,toWrite))
	#		fileOut.write(toWrite)
	fileOut.write("Hi!\n")
	fileOut.write("Hi again!")