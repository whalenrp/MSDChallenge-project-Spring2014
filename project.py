#!/usr/bin/env python

import sys
import argparse
from CollaborativeModelPredictor import CollaborativeModelPredictor
from CollaborativeMemoryPredictor import CollaborativeMemoryPredictor

def main(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-train_file', default='sanitized_data.txt',
		help='A file of existing user data')
	parser.add_argument('-predict_file', default='kaggle_users.txt',
		help='A file containing the list of users to predict songs for')
	parser.add_argument('-output_file', default='output_data.txt',
		help='The file to output predictions')
	parser.add_argument('-collaborative_mode', required=True, choices=['model','memory'],
		help='The type of algorithm to use: user-centric or item-centric')
	parser.add_argument('-alpha', required=True, help='The alpha exponent used in weighting probabilities')
	parser.add_argument('-exponent', required=True, 
		help='With increasing value, decreases the weighting of	neighbors further from a given user')
	values = vars(parser.parse_args())

	# Based on our algorithm, build the corresponding strategy and predict results on it.
	predictor = None
	if values['collaborative_mode'] == 'model':
		predictor = CollaborativeModelPredictor(values['train_file'], values['predict_file'], values['output_file'],
			values['alpha'], values['exponent'])
	else:
		predictor = CollaborativeMemoryPredictor(values['train_file'], values['predict_file'], values['output_file'],
			values['alpha'], values['exponent'])
	predictor.predictAll()
pass


if __name__=='__main__':
	main(sys.argv)
