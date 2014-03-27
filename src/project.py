#!/usr/bin/env python

import time
import sys
import argparse
from CollaborativeUsersPredictor import CollaborativeUsersPredictor
from CollaborativeItemsPredictor import CollaborativeItemsPredictor

def main(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-train_file', default='../data/EvalDataYear1MSDWebsite/year1_test_triplets_hidden.txt',
		help='A file of existing user data')
	parser.add_argument('-predict_file', default='../data/EvalDataYear1MSDWebsite/year1_test_triplets_visible.txt',
		help='A file containing the list of users to predict songs for')
	parser.add_argument('-output_file', default='../data/output_data.txt',
		help='The file to output predictions')
	parser.add_argument('-mode', default = 'users', choices=['users','items'],
		help='The type of algorithm to use: user-centric or item-centric')
	parser.add_argument('-a', required=True, help='The alpha exponent used in weighting probabilities')
	parser.add_argument('-q', required=True, 
		help='With increasing value, decreases the weighting of	neighbors further from a given user')
	values = vars(parser.parse_args())

	# Based on our algorithm, build the corresponding strategy and predict results on it.
#	predictor = None
#	if values['mode'] == 'users':
#		predictor = CollaborativeUsersPredictor(values['train_file'], values['predict_file'], values['output_file'],
#			values['a'], values['q'])
#	else:
#		predictor = CollaborativeItemsPredictor(values['train_file'], values['predict_file'], values['output_file'],
#			values['a'], values['q'])
#	predictor.predictAll()
	predictors = list()
	predictors.append(CollaborativeUsersPredictor(values['train_file'], values['predict_file'], values['output_file'],
		values['a'], values['q']))
	predictors.append(CollaborativeItemsPredictor(values['train_file'], values['predict_file'], values['output_file'],
		values['a'], values['q']))

	for p in predictors:
		print p.getType()
		print "\tmAP@500\t\ta\t\tq\titer\tsec"
		for q in range(2,7):
			for a in range(1, 10):
				alpha = a/10.0
				iterations = 5000
				p.alpha = alpha
				p.exponent = q
				t0 = time.time()
				mAP = p.predictAll(iterations)
				print "\t%0F\t%0F\t%0d\t%0d\t%0F" %( mAP, p.alpha, p.exponent, iterations, time.time() - t0)
				#, mAP, "\t", p.alpha, "\t", p.exponent, "\t", iterations, "\t", time.time() - t0 


if __name__=='__main__':
	main(sys.argv)
