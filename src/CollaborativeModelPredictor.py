import sys # used for debugging temporarily
from AbstractPredictor import AbstractPredictor
from scipy.sparse import coo_matrix


class CollaborativeModelPredictor(AbstractPredictor):

	def __init__(self, training_file, predict_file, output_file, alpha, exponent):
		AbstractPredictor.__init__(self, training_file, predict_file, 
			output_file, alpha, exponent)
		pass

	def predict(self, userId):
		"""
		Given the id of a user from the kaggle_users file, this method
		will compare this user to every other user, aggregating their 
		preferences together to provide a list of the top 500 recommendations.
		"""

		# Find the listening history of the provided user
		uVec = None
		with open(self.training_file, 'r') as f:
			for line in f:
				if line.split(' ')[0] == userId:
					uVec = self.getKeysFromLine(line)
			pass

		# Sanity check
		if uVec is None: 
			raise Exception("The user has no data in the training file")

		# Now, compare the current user 'u' to all other users 'v', 
		# using their preferences to judge their weighting in our 
		# recommendation system
		numSongs = self.getNumberSongs()
		item_values_vector = coo_matrix((1,numSongs))
		with open(self.training_file, 'r') as f:
			for line in f:
				if not line.split(' ')[0] == userId:
					vVec = self.getKeysFromLine(line)
					weighting = self.getUserWeighting(uVec, vVec)
					if not weighting == 0.0:
						weights = [weighting]* len(vVec)
						row = [0] * len(vVec)
						item_values_vector = item_values_vector + \
							coo_matrix((weights,(row, map(lambda s: s-1, vVec))), shape=(1,numSongs))
						
				pass
			pass

		# Take the sparse vector of item scores, sort the non-zero entries by score,
		# and return the first 500 song ids corresponding to each score.
		item_values_vector = coo_matrix(item_values_vector)
		sorted_results = sorted(zip(item_values_vector.data, item_values_vector.col), reverse=True)

		songs_to_recommend = []
		for _,songId in sorted_results:
			if len(songs_to_recommend) >= 500:
				break
			if not int(songId)+1 in uVec:
				songs_to_recommend.append(str(songId+1))
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

	def getKeysFromLine(self, string):
		"""
		Given a line of data in the format 'userId songNumber:1 ...'
		this method returns a list of every songNumber value for 
		later use in creating a sparse matrix
		"""
		pairs = string.split(' ', 1)[1].split(' ')
		return map(lambda x: int(x.split(':')[0]), pairs)

	def getNumberSongs(self):
		with open("../data/kaggle_songs.txt") as f:
			for i, l in enumerate(f):
				pass
			return i + 1
