import Utils
from pyspark import SparkContext

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
		user2songs = Utils.usersToSongs(self.training_file, "../data/kaggle_songs.txt")
		user2songs_hidden = Utils.usersToSongs(self.predict_file, "../data/kaggle_songs.txt", True);

		sc = SparkContext("spark://ip-172-31-41-158:7077", "testingPredictions", "/home/ec2-user/spark-0.9.1", 
			["../data/kaggle_songs.txt", "../data/kaggle_visible_evaluation_triplets.txt", "../data/kaggle_users.txt"])
		user2songs = sc.parallelize(user2songs.items())
		user2songs.map(lambda (x,y): self.predict(y)).saveAsTextFile("sparktest")
	#	outWriter = open(self.output_file, 'w')
	#	AP = float (0);
	#	i = 1;
	#	for userId,userSongs in user2songs.items():
	#		results = self.predict(userSongs)
	#		outWriter.write(' '.join(results) + '\n')

	#		AP += float(Utils.AP(results, user2songs_hidden[userId], 500))
	#		print i, " mAP: ", AP/float(i)
	#		i +=float(1)
	#	outWriter.close()
			
		pass

	def getUserListeningHistories(self):
		"""
		Returns a list of lists where each sublist consists of the
		listening history (list of song ids) for one user.
		"""
		user2songs = list()
		with open(self.training_file) as f:
			for line in f:
				user2songs.append(self.getKeysFromLine(line))
			pass
		return user2songs
		

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
