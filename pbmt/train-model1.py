from collections import defaultdict,namedtuple
from itertools   import product,repeat
import sys
import numpy as np
import time
import math


def maximum_alignment(i):
    possible_alignments = [(j, self.t[(f[i], e[j])]) for j in range(0, l)]
    return max(possible_alignments, key=lambda x: x[1])[0]


with open(sys.argv[1], "r") as infile_f:
  f_sents = [ line.strip().split() for line in infile_f ]
with open(sys.argv[2], "r") as infile_e:
  e_sents = [ line.strip().split() for line in infile_e ]

corpus = zip(f_sents,e_sents)
lens = set()
aligns = defaultdict(set)

# "Compute all possible alignments..."
for k, (f, e) in enumerate(corpus):
    e = [None] + e
    lens.add((len(e), len(f) + 1))
    for (f, e) in product(f, e):
        aligns[e].add((f, e))

# "Compute initial probabilities for each alignment..."
t = dict()
g = lambda n: [1 / float(n)] * n
for e, aligns_to_e in aligns.iteritems():
    p_values = g(len(aligns_to_e))
    t.update(zip(aligns_to_e, p_values))





for time in range(5):   
    likelihood = 0.0
    c1 = defaultdict(float) # ei aligned with fj
    c2 = defaultdict(float) # ei aligned with anything

    # The E-Step
    for k, (f, e) in enumerate(corpus):

       
        e = [None] + e
        l = len(e)
        m = len(f) + 1
        q = 1 / float(l)

        for i in range(1,m):

            num = [ q * t[(f[i - 1], e[j])] for j in range(0,l) ]
            den = float(sum(num))
            #print 'i',k,i,'den',den, 'num',num
            likelihood += math.log(den)

            for j in range(0, l):

                delta = num[j] / den

                c1[(f[i - 1], e[j])] += delta
                c2[(e[j],)]      += delta

    # The M-Step
    t = defaultdict(float, {
        k: v / c2[k[1:]]
        for k, v in c1.iteritems() if v > 0.0 })
    #print likelihood

with open(sys.argv[3], "w") as outfile:
    for (f,e) in corpus:
        e = [None] + e 
        l = len(e)
        m = len(f)+1
        for i in range(1,m):
            possible_alignments = [(j, t[(f[i-1], e[j])]) for j in range(l)]
            max_align = max(possible_alignments, key=lambda x: x[1])[0]
            #print possible_alignments,max_align
            
            outfile.write(str(max_align)+'-'+str(i-1)+' ')
        outfile.write('\n')
