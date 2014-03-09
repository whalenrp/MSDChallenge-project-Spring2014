from AbstractPredictor import AbstractPredictor

class CollaborativeMemoryPredictor(AbstractPredictor):

	def __init__(self, training_file, predict_file, output_file, alpha, exponent):
		AbstractPredictor.__init__(self, training_file, predict_file, 
			output_file, alpha, exponent)
		pass

	def predict(self, userId):
		return list(['1','2','3'])
