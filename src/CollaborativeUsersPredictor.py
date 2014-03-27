import sys # used for debugging temporarily
import time
import Utils
from AbstractPredictor import AbstractPredictor
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix


class CollaborativeUsersPredictor(AbstractPredictor):

	def __init__(self, training_file, predict_file, output_file, alpha, exponent):
		AbstractPredictor.__init__(self, training_file, predict_file, 
			output_file, alpha, exponent)
		self.user2songs = Utils.usersToSongs(self.training_file, "../data/kaggle_songs.txt").values()
		pass

	def predict(self, uVec):
		"""
		Given a list of song id's that a user has listened to, this method
		will compare this user to every other user, aggregating their 
		preferences together to provide a list of the top 500 recommendations.
		"""

		# Now, compare the current user 'u' to all other users 'v', 
		# using their preferences to judge their weighting in our 
		# recommendation system
		results = dict()
		for vVec in self.user2songs:
			weighting = self.getUserWeighting(uVec, vVec)
			if weighting == 0.0:
				continue
			for song in vVec:
				if song in results: results[song] += weighting
				else: results[song] = weighting
				
		# Take the dict of item scores, sort the non-zero entries by score,
		# and return the first 500 song ids corresponding to each score.
		sorted_results = sorted(zip(results.values(), results.keys()), reverse=True)


		songs_to_recommend = []
		for _,songId in sorted_results:
			if len(songs_to_recommend) >= 500:
				break
			if not int(songId) in uVec:
				songs_to_recommend.append(str(int(songId)))
			pass

		return songs_to_recommend

	def getUserWeighting(self, u1, u2):
		"""
		This function returns a variation of the cosign of similarity function
		by raising the factors in the denominator to the class parameters for
		alpha and (1 - alpha), and raising the result to the self.exponent power
		"""
		intersectSize = float(len(set(u1) & set(u2)))
		if intersectSize == 0 : return 0.0
		weight = intersectSize / (len(u1)**self.alpha * len(u2)**(1.0 - self.alpha))
		return weight**self.exponent

	def getNumberSongs(self):
		with open("../data/kaggle_songs.txt") as f:
			for i, l in enumerate(f):
				pass
		return i+1

	def getType(self):
		return "CollaborativeUsersPredictor"
