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

	predictors = list()
	predictors.append(CollaborativeUsersPredictor(values['train_file'], values['predict_file'], values['output_file'],
		values['a'], values['q']))
	predictors.append(CollaborativeItemsPredictor(values['train_file'], values['predict_file'], values['output_file'],
		values['a'], values['q']))

	startTime = time.time()
	outFile = open(values['output_file'], 'w', 1)
	for p in predictors:
		outFile.write( p.getType() + "\n")
		outFile.write("\tmAP@500\t\ta\t\tq\titer\tsec\n")
		for q in range(2,7):
			for a in range(1, 10):
				alpha = a/10.0
				iterations = 400 
				p.alpha = alpha
				p.exponent = q
				t0 = time.time()
				mAP = p.predictAll(iterations)
				outFile.write("\t{0:.5f}\t{1:.1f}\t{2}\t{3}\t{4:.2f}\n".format( mAP, p.alpha, p.exponent, iterations, time.time() - t0))
	print "Finished in ", time.time() - startTime, " seconds"


if __name__=='__main__':
	main(sys.argv)
