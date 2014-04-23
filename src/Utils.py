# Functions copied from http://www.math.unipd.it/~aiolli/CODE/MSD/
#       F. Aiolli, A Preliminary Study on a Recommender System for the Million Songs Dataset Challenge
#       Preference Learning: Problems and Applications in AI (PL-12), ECAI-12 Workshop, Montpellier
#       http://www.ke.tu-darmstadt.de/events/PL-12/papers/08-aiolli.pdf 

basePath = '/home/ubuntu/MSDChallenge-project-Spring2014'

def usersToSongs(ifstream, songMappingFile, asSet=False):
	user_to_songs = dict();
	songsToId = song_to_idx(songMappingFile);
	with open(ifstream) as f:
		for line in f:
			user, song, _ = line.split('\t')
			if user in user_to_songs:
				if asSet:
					user_to_songs[user].add(int(songsToId[song]));
				else:
					user_to_songs[user].append(int(songsToId[song]));
			else:
				if asSet:
					user_to_songs[user] = set([int(songsToId[song])]);
				else:	
					user_to_songs[user] = list([int(songsToId[song])]);
	return user_to_songs

#l_rec: list of recommended songs
#u2s: mapping users to songs
#tau: 500
def AP(l_rec, sMu, tau):

    np=len(sMu)
    nc=0.0
    mapr_user=0.0
    for j,s in enumerate(l_rec):
        if j>=tau:
            break
        if int(s) in sMu:
            #print "s in sMu"
            nc+=1.0
            mapr_user+=nc/(j+1)
    mapr_user/=min(np,tau)
    return mapr_user

#l_users: list of users
#l_rec_songs: list of lists, recommended songs for users
#u2s: mapping users to songs
#tau: 500
def mAP(l_users, l_rec_songs, u2s, tau):
    mapr=0
    n_users=len(l_users)
    for i,l_rec in enumerate(l_rec_songs):
        if not l_users[i] in u2s:
            continue
        mapr+=AP(l_rec,u2s[l_users[i]], tau)
    return mapr/n_users

def song_to_idx(if_str):
     with open(if_str,"r") as f:
         sti=dict(map(lambda line: line.strip().split(' '),f.readlines()))
     return sti

def songs2users(listenHistFile, songsFile):
	songs2ids = song_to_idx(songsFile)
	#songs2users = dict(map(lambda x: (int(x), set()), songs2ids.values()))
	songs2users = dict()
	with open(listenHistFile) as f:
		for line in f:
			user, song, _ = line.strip().split('\t')
			songId = int(songs2ids[song])
			if songId in songs2users:
				songs2users[songId].add(user)
			else:
				songs2users[songId] = set([user])

	return songs2users
