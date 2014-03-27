from AbstractPredictor import AbstractPredictor
import Utils

class CollaborativeItemsPredictor(AbstractPredictor):

	def __init__(self, training_file, predict_file, output_file, alpha, exponent):
		AbstractPredictor.__init__(self, training_file, predict_file, 
			output_file, alpha, exponent)
		self.songs2users = Utils.songs2users(self.training_file,"../data/kaggle_songs.txt")
		self.users2ids(self.songs2users)
		pass

	def users2ids(self, songs2users):
		user2id = dict()
		userCount = 1
		for songId, users in songs2users.items():
			newUserList = set()
			for user in users:
				if not user in user2id:
					user2id[user] = userCount;
					userCount+=1
				newUserList.add(user2id[user])
			songs2users[songId] = newUserList
					
			

	def predict(self, userSongs):
		songScores = dict()
		for s, users in self.songs2users.items():
			if len(users) == 0:
				continue
			userSet = set(users)
			songScores[s] = 0.0
			for user_song in userSongs:
				songScores[s] += self.scoreSong(userSet, self.songs2users[user_song])
				pass

		sorted_results = sorted(zip(songScores.values(), songScores.keys()), reverse=True)


		songs_to_recommend = []
		for _,songId in sorted_results:
			if len(songs_to_recommend) >= 500:
				break
			if not int(songId) in userSongs:
				songs_to_recommend.append(str(int(songId)))
			pass

		return songs_to_recommend

	def scoreSong(self, a, b):
		intersectSize = float(len(a & b))
		if intersectSize == 0 : return 0.0
		weight = intersectSize / (len(a)**self.alpha * len(b)**(1.0 - self.alpha))
		return weight**self.exponent

	def getType(self):
		return "CollaborativeItemsPredictor"
