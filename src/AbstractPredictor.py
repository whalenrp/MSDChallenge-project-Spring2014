
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

		outWriter = open(self.output_file, 'w')
		userFile = open(self.predict_file, 'r')
		for line in userFile:
			results = self.predict(line.strip())
			outWriter.write(' '.join(results) + '\n')
		userFile.close()
		outWriter.close()
		pass

	def predict(self, userId):
		raise Exception('Abstract class cannot be instantiated')
