
class AbstractPredictor( object ):
	""" 
	This class serves as an abstract base class for music recommendation predictors. 
	Subclasses of this class must implement the 'predict' method for providing music
	suggestions for a given user. 
	Predict should return a sorted list of the top 500 recommendations for a given user as strings
	"""

	def __init__(self, training_file, predict_file, output_file, alpha, exponent):
		if self.__class__ is AbstractPredictor:
			raise TypeError('Abstract class cannot be instantiated')
		self.training_file = training_file
		self.predict_file = predict_file
		self.output_file = output_file
		self.alpha = float(alpha)
		self.exponent = int(exponent)

	def predictAll(self):

		# Build a list of lists containing song histories
		# for each user.
		user2songs = list()
		with open(self.training_file) as f:
			for line in f:
				user2songs.append(self.getKeysFromLine(line))
			pass

		outWriter = open(self.output_file, 'w')
		userFile = open(self.training_file, 'r')
		for line in userFile:
			results = self.predict(self.getKeysFromLine(line), user2songs)
			outWriter.write(' '.join(results) + '\n')
		userFile.close()
		outWriter.close()
		pass

	def predict(self, userId):
		raise Exception('Abstract class cannot be instantiated')

	def getKeysFromLine(self, string):
		"""
		Given a line of data in the format 'userId songNumber:1 ...'
		this method returns a list of every songNumber value for 
		later use in creating a sparse matrix
		"""
		pairs = string.split(' ', 1)[1].split(' ')
		return map(lambda x: int(x.split(':')[0]), pairs)
