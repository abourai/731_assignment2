# -*- encoding: utf-8 -*-
import sys
from collections import defaultdict
import math

'''
Determine whether set of values is quasi-consecutive
  Examples:
	{1, 2, 3, 4, 5, 6} => True
	{4, 2, 3} => True (equivalent to {2, 3, 4})
	{3} => True
	{1, 2, 4} => True if word at position 3 is not aligned to anything, False otherwise
'''
def quasi_consec(tp, aligned_words):
  return sorted(tp) == range(min(tp), max(tp)+1)


def check_sp(i1, i2, sp):
	for p in sp:
		if p < i1 or p > i2:
			return False
	return True

'''
Given an alignment, extract phrases consistent with the alignment
  Input:
	-e_aligned_words: mapping between E-side words (positions) and aligned F-side words (positions)
	-f_aligned_words: mapping between F-side words (positions) and aligned E-side words (positions)
	-e: E sentence
	-f: F sentence
  Return list of extracted phrases
'''
def phrase_extract(e_aligned_words, f_aligned_words, e, f):
  extracted_phrases = []
  # Loop over all substrings in the E
  for i1 in range(len(e)):
	for i2 in range(i1, len(e)):
	  # Get all positions in F that correspond to the substring from i1 to i2 in E (inclusive)
	  tp = []

	  for alignment in f_aligned_words:
		  #print alignment
		  if alignment[0] >= i1 and alignment[0] <= i2:
			  tp.append(alignment[1])
#	  	print tp, quasi_consec(tp, f_aligned_words)
	 # continue
	  if len(tp) != 0 and quasi_consec(tp, f_aligned_words):
		j1 = min(tp) # min TP
		j2 = max(tp) # max TP
		# Get all positions in E that correspond to the substring from j1 to j2 in F (inclusive)
		sp = []
		for e_align in e_aligned_words:
		#	print e_align
			if e_align[0] >= j1 and e_align[0] <= j2:
				sp.append(e_align[1])
		if len(sp) != 0 and check_sp(i1, i2, sp): # Check that all elements in sp fall between i1 and i2 (inclusive)
		  e_phrase = e[i1:i2+1]
		  f_phrase = f[j1:j2+1]
		  if (i2+1 - i1) <= 3 and (j2+1 - j1) <=3:
			extracted_phrases.append((e_phrase, f_phrase))
		  # Extend source phrase by adding unaligned words
		#   while j1 >= 0 and TODO: # Check that j1 is unaligned
		# 	j_prime = j2
		# 	while j_prime < len(f) and TODO: # Check that j2 is unaligned
		# 	  f_phrase = f[j1:j_prime+1]
		# 	  extracted_phrases.append((e_phrase, f_phrase))
		# 	  j_prime += 1
		# 	j1 -= 1

  return extracted_phrases


def calculate_probs(extracted_phrases, output):
	count_f = defaultdict(lambda: defaultdict(int))
	count_e = defaultdict(lambda: defaultdict(int))
	total_f = defaultdict(float)
	total_e = defaultdict(float)

	for (f, e) in extracted_phrases:
		f = ' '.join(f)
		e = ' '.join(e)
		count_f[f][e] += 1
		count_e[e][f] += 1

		total_f[f] += 1
		total_e[e] += 1

	write_p = open(output, 'wb')
	for e in count_e:
		for f in count_e[e]:
		#	print e, f, abs(math.log(float(count_e[e][f]) / total_f[f]))
			write_p.write('{}\t{}\t{}\n'.format(e, f, abs(math.log(float(count_e[e][f]) / total_f[f]))))



def read_bitext(source, target):

	bitext = []
	with open(target) as tgt_f:

		for line in tgt_f.readlines():
			bitext.append([line.rstrip().split()])

	with open(source) as src_f:
		src_sents = src_f.readlines()
		for i in xrange(len(src_sents)):
		#	print bitext[i]
			bitext[i].append(src_sents[i].rstrip().split())

	return bitext


def read_alignments(f_file):
	e_alignments = []
	f_alignments = []
	with open(f_file) as f_align:

		for line in f_align.readlines():
			f_sent = []
			e_sent = []
			pointers = line.rstrip().split()
			for pointer in pointers:
				f_sent.append((int(pointer.split('-')[0]), int(pointer.split('-')[1])))
				e_sent.append((int(pointer.split('-')[1]), int(pointer.split('-')[0])))

			f_alignments.append(f_sent)
			e_alignments.append(e_sent)

	return e_alignments, f_alignments


def main(args):
	bitext = read_bitext(args[1], args[2])
	e_alignments, f_alignments = read_alignments(args[3])

	extracted_phrases = []
	for idx, (e, f) in enumerate(bitext):
		e_aligned_words = e_alignments[idx]
		f_aligned_words = f_alignments[idx]

		extracted_phrases += phrase_extract(e_aligned_words, f_aligned_words, e, f)

	#print extracted_phrases
	#write_p = open('test_phrase.txt')
	#for
	calculate_probs(extracted_phrases, args[4])


if __name__=='__main__':
	sys.exit(main(sys.argv))
