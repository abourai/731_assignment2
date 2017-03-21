from collections import defaultdict,namedtuple
from itertools   import product,repeat
import sys
import numpy as np
import time
import math

from ibm1 import IBM, read_bitext_file


def read_params():
    bitext = read_bitext_file(sys.argv[1], sys.argv[2])
    ibm = IBM(bitext, max_iter=8)
    params = ibm.train()
    keys = params.keys()
    new_theta = {(x[1], x[0]): params[x] for x in keys}
    return new_theta


def read_t():
    return np.load(sys.argv[4]+'.npy').item()



def alignment(f_sents,e_sents,f_name):
    corpus = zip(f_sents,e_sents)
    lens = set()
    aligns = defaultdict(set)

    for k, (f, e) in enumerate(corpus):
        #e = [None] + e
        lens.add((len(e), len(f) + 1))
        for (f, e) in product(f, e):
            aligns[e].add((f, e))

    t = read_params()
    #t = read_t()
    g = lambda n: [1 / float(n)] * n
    # for e, aligns_to_e in aligns.iteritems():
    #     p_values = g(len(aligns_to_e))
    #     t.update(zip(aligns_to_e, p_values))
    q = dict()
    for k, (l, m) in enumerate(lens):
        for i in range(0, m):
            p_values = g(l)
            for j in range(0, l):
                q[(j, i, l, m)] = p_values[j]


    for time in range(10):
        likelihood = 0.0
        c1 = defaultdict(float) # ei aligned with fj
        c2 = defaultdict(float) # ei aligned with anything
        c3 = defaultdict(float)
        c4 = defaultdict(float)
        print time
        # The E-Step
        for k, (f, e) in enumerate(corpus):
            #e = [None] + e
            l = len(e) #+ 1
            m = len(f) + 1
            for i in range(1,m):
                num = [ q[(j,i,l,m)] * t[(f[i - 1], e[j])] for j in range(l) ]
                den = float(sum(num))
                likelihood += math.log(den)
                for j in range(0, l):
                    delta = num[j] / den
                    c1[(f[i - 1], e[j])] += delta
                    c2[(e[j],)]          += delta
                    c3[(j, i, l, m)]     += delta
                    c4[(i, l, m)]        += delta
        # The M-Step
        t = defaultdict(float, {k: v / c2[k[1:]] for k, v in c1.iteritems() if v > 0.0})
        q = defaultdict(float, {k: v / c4[k[1:]] for k, v in c3.iteritems() if v > 0.0})
        print likelihood / 24901
    #final_align = defaultdict(lambda: defaultdict(int))

    with open(f_name, "w") as outfile:
        for index,(f,e) in enumerate(corpus):
            #e = [None] + e
            l = len(e)#+1
            m = len(f)+1
            for i in range(1,m):
                alignments = [(j, t[(f[i - 1], e[j])] * q[(j, i, l, m)]) for j in range(l)]
                max_align = max(alignments, key=lambda x: x[1])[0]

                outfile.write(str(max_align)+'-'+str(i-1)+' ')
                #final_align[index][i-1] = max_align
            outfile.write('\n')
    return #final_align

with open(sys.argv[1], "r") as infile_f:
  f_sents = [ line.strip().split() for line in infile_f ]
with open(sys.argv[2], "r") as infile_e:
  e_sents = [ line.strip().split() for line in infile_e ]

aligns_f = alignment(f_sents,e_sents,sys.argv[3])
#print read_params()
#aligns_e = alignment(e_sents,f_sents,'alignment_e.txt')


# aligns_intersect = defaultdict(lambda: defaultdict(int))
# aligns_union     = defaultdict(lambda: defaultdict(int))

# for k in aligns_f:
#     for j in aligns_f[k]:
#         if aligns_e[k][aligns_f[k][j]] == j:
#             aligns_intersect[k][str(aligns_f[k][j])+'-'+str(j)] = 1

# for k in aligns_f:
#     for j in aligns_f[k]:
#         aligns_union[k][str(aligns_f[k][j])+'-'+str(j)] = 1
# for k in aligns_e:
#     for i in aligns_e[k]:
#         aligns_union[k][str(i)+'-'+str(aligns_e[k][i])] = 1

# with open('aligns_union.txt',"w") as outfile:
#     for k in aligns_union:
#         for align in aligns_union[k]:
#             outfile.write(align+' ')
#         outfile.write('\n')
# with open('aligns_intersection.txt',"w") as outfile:
#     for k in aligns_intersect:
#         for align in aligns_intersect[k]:
#             outfile.write(align+' ')
#         outfile.write('\n')
