# -*- encoding: utf-8 -*-

import sys
from collections import defaultdict
import numpy as np
import math
'''
  Alignment: P( E | F) = Σ_θ P( θ, F | E) (Equation 98)
  IBM model 1: P( θ, F | E)
  (1) Initialize θ[i,j] = 1 / (|E| + 1) (i for E and j for F) (Equation 100)
  (2) Expectation-Maximization (EM)
	[E] C[i,j] =  θ[i,j] / Σ_i θ[i,j] (Equation 110)
	[M] θ[i,j] =  C[i,j] / Σ_j C[i,j] (Equation 107)
  (3) Calculate data likelihood (Equation 106)
'''

class IBM():
  def __init__(self, bitext, max_iter = 5):
	self.bitext = bitext
	self.max_iter = max_iter
	self.tgt_vocab = defaultdict(lambda: 0)
	self.src_vocab = defaultdict(lambda: 0)
	self.max_f = 0
	for (e,f) in self.bitext:
		if len(f) > self.max_f: self.max_f = len(f)
		for e_word in e:
			self.tgt_vocab[e_word] += 1
		for f_word in f:
			self.src_vocab[f_word] += 1

  def likelihood(self):
	  L = 0
	  x = 0
	  for (e,f) in self.bitext:

		  for j in xrange(len(f)):
			  temp = 0
			  for i in xrange(len(e)):
				 # print e[i], f[j]
				  temp += self.theta[e[i], f[j]] / len(e)
				  #print len(self.word_freq), len(e)
			  L += math.log(temp)
	  return L / 19099#* (1.0/self.max_f)

  def train(self):
	# (1) Initialize θ[i,j] = 1 / (|E| + 1) (Equation 100)
	initial_prob = 1.0 / len(self.tgt_vocab.keys())
#	print len(self.tgt_vocab.keys())
	# e = [words[0] for words in self.bitext][0]
	# f = [words[1] for words in self.bitext][0]

	self.theta = defaultdict(lambda: initial_prob)

	for num in range(self.max_iter):
	  # (2) [E] C[i,j] = θ[i,j] / Σ_i θ[i,j] (Equation 110)
	 # print count
		print num
		count = defaultdict(lambda: 0.0)
		total_f = defaultdict(lambda: 0.0)
		for (e, f) in self.bitext:

		#	print e
		#	print f
			total_e = defaultdict(lambda: 0.0)
			for j in xrange(len(f)):
				for i in xrange(len(e)):
					total_e[e[i]] += self.theta[e[i], f[j]]

		#	total_f = defaultdict(float)
			for j in xrange(len(f)):
				for i in xrange(len(e)):
					count[e[i], f[j]] += self.theta[e[i], f[j]] / total_e[e[i]]
					total_f[f[j]] += self.theta[e[i], f[j]] / total_e[e[i]]

		# (2) [M] θ[i,j] =  C[i,j] / Σ_j C[i,j] (Equation 107)
		# for (e,f) in self.bitext:
		# 	for f_word in f:
		# 		for e_word in e:
		# 		#	print e[i], f[j]
		# 			self.theta[e_word, f_word] = count[e_word, f_word] / total_f[f_word]
		# 			#print (e[i], f[j]), count[(e[i], f[j])] / total_f[f[j]]
		for (e_word, f_word) in self.theta.keys():
			self.theta[e_word, f_word] = count[e_word, f_word] / total_f[f_word]
	#print self.theta
	  #self.theta[ e[i], f[j] ] = TODO
	  # (3) Calculate log data likelihood (Equation 106)
		ll = self.likelihood()
		#print len(self.theta.keys())
		print '[' + str(num) + ']', 'Log Likelihood:', ll
	return self.theta


  def _argmax(self, e, word):
	  max_prob = 0
	  max_j = None
	  index = None
	  for i in xrange(len(e)):
		  if self.theta[e[i], word] > max_prob:
			  max_j = e[i]
			  index = i
			  max_prob = self.theta[e[i], word]
			 # print word, max_j, max_prob
	  #if max_j != None:
		#print word, max_j, max_prob
	  return index, max_j, max_prob


  def align(self, output):
	alignments = []
	alignment_f = open(output, 'wb')
	for idx, (e, f) in enumerate(self.bitext):
	#	print e
	#	print f
		alignment_line = ''
		for j in range(len(f)):
			# ARGMAX_j θ[i,j] or other alignment in Section 11.6 (e.g., Intersection, Union, etc)
			index, max_j, max_prob = self._argmax(e, f[j])
		#	print f[j], max_j, max_prob
			alignment_line += str(index) + '-' + str(j) + ' '
			#print self.theta[(e[i], _)]
			#self.plot_alignment((max_j, max_prob), e, f)
		alignment_f.write(alignment_line + '\n')
	return alignments


def read_bitext_file(source, target):

	bitext = []
	with open(target) as tgt_f:

		for line in tgt_f.readlines():
			bitext.append([line.rstrip().split()])

	with open(source) as src_f:
		src_sents = src_f.readlines()
		for i in xrange(len(src_sents)):
		#	print bitext[i]
			bitext[i].append(src_sents[i].rstrip().split())

	#print bitext
	return bitext


def main(args):

  bitext = read_bitext_file(args[1], args[2])
  # bitext = [ ( ['with', 'vibrant', ..], ['mit', 'hilfe',..] ), ([], []) , ..]
  ibm = IBM(bitext, max_iter = 8)
  ibm.train()
  ibm.align(args[3])

if __name__ == '__main__':
	sys.exit(main(sys.argv))
