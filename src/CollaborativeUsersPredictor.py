import sys # used for debugging temporarily
import time
from AbstractPredictor import AbstractPredictor
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix


class CollaborativeUsersPredictor(AbstractPredictor):

	def __init__(self, training_file, predict_file, output_file, alpha, exponent):
		AbstractPredictor.__init__(self, training_file, predict_file, 
			output_file, alpha, exponent)
		self.numSongs = self.getNumberSongs()
		pass

	def predict(self, uVec, user2songs =None):
		"""
		Given a list of song id's that a user has listened to, this method
		will compare this user to every other user, aggregating their 
		preferences together to provide a list of the top 500 recommendations.
		"""

		if user2songs is None:
			user2songs = Utils.usersToSongs(self.training_file, "../data/kaggle_songs.txt").values()

		# Now, compare the current user 'u' to all other users 'v', 
		# using their preferences to judge their weighting in our 
		# recommendation system
		item_values_vector = csr_matrix((1,self.numSongs))
		for vVec in user2songs:
			weighting = self.getUserWeighting(uVec, vVec)
			if not weighting == 0.0:
				weights = [weighting]* len(vVec)
				row = [0] * len(vVec)
				item_values_vector = item_values_vector + \
					csr_matrix((weights,(row, map(lambda s: s-1, vVec))), shape=(1,self.numSongs))

		# Take the sparse vector of item scores, sort the non-zero entries by score,
		# and return the first 500 song ids corresponding to each score.
		item_values_vector = coo_matrix(item_values_vector)
		sorted_results = sorted(zip(item_values_vector.data, item_values_vector.col), reverse=True)


		songs_to_recommend = []
		for _,songId in sorted_results:
			if len(songs_to_recommend) >= 500:
				break
			if not int(songId)+1 in uVec:
				songs_to_recommend.append(str(int(songId)+1))
			pass

		return songs_to_recommend

	def getUserWeighting(self, u1, u2):
		"""
		This function returns a variation of the cosign of similarity function
		by raising the factors in the denominator to the class parameters for
		alpha and (1 - alpha), and raising the result to the self.exponent power
		"""
		intersectSize = float(len(set(u1) & set(u2)))
		weight = intersectSize / (len(u1)**self.alpha * len(u2)**(1.0 - self.alpha))
		return weight**self.exponent

	def getNumberSongs(self):
		with open("../data/kaggle_songs.txt") as f:
			for i, l in enumerate(f):
				pass
		return i+1
