from collections import defaultdict,namedtuple
from itertools   import product,repeat
import sys
import numpy as np
import time
import math



def calculate_probs(extracted_phrases, output):
    count_f = defaultdict(lambda: defaultdict(int))
    count_e = defaultdict(lambda: defaultdict(int))
    total_f = defaultdict(float)
    total_e = defaultdict(float)

    for (f, e) in extracted_phrases:
        count_f[f][e] += 1
        count_e[e][f] += 1

        total_f[f] += 1
        total_e[e] += 1

    write_p = open(output, 'wb')
    for e in count_e:
        for f in count_e[e]:
            #print e, f, abs(math.log(float(count_e[e][f]) / total_f[f]))
            write_p.write('{}\t{}\t{}\n'.format(f, e, abs(math.log(float(count_e[e][f]) / total_f[f]))))


def consecutive(set1,k,dict1):
    if len(set1) == 0:
        return False
    i = min(set1)
    j = max(set1)
    for m in range(i,j+1):
        if m not in set1 and dict1[k][m] != 0:
            return False
    return True


with open(sys.argv[1], "r") as infile_f:
  f_sents = [ line.strip().split() for line in infile_f ]
with open(sys.argv[2], "r") as infile_e:
  e_sents = [ line.strip().split() for line in infile_e ]

corpus = zip(f_sents,e_sents)
align_f = defaultdict(lambda: defaultdict(int))
align_e = defaultdict(lambda: defaultdict(int))

with open(sys.argv[3]) as f_align:
    line_num = 0
    for line in f_align.readlines():
        pointers = line.rstrip().split()
        for pointer in pointers:
            #print line_num
            align_f[line_num][int(pointer.split('-')[1])] =int(pointer.split('-')[0])
            align_e[line_num][int(pointer.split('-')[0])] =int(pointer.split('-')[1])
        line_num += 1


phrase = []
for k,(f,e) in enumerate(corpus):
    #print ' '.join(f[0:3])
    for i1 in range(len(e)):
        for i2 in range(i1,min(len(e),i1+3)):
            tp = set()
            for i in range(i1,i2+1):
                tp.add(align_e[k][i+1])
            if consecutive(tp,k,align_f):
                j1 = min(tp)
                j2 = max(tp)
                sp = set()
                for j in range(j1,j2+1):
                    if align_f[k][j] > 0:
                        sp.add(align_f[k][j] - 1)
                if len(sp)>0 and min(sp)>=i1 and max(sp)<=i2:
                    phrase.append( (" ".join(f[j1:j2+1])," ".join(e[i1:i2+1])))
                    while j1 >= 0 and align_f[k][j1]==0:
                        j_prime = j2
                        while j_prime < len(f) and align_f[k][j_prime]==0:
                            phrase.append((" ".join(f[j1:j_prime+1]), " ".join(e[i1:i2+1])))
                            j_prime += 1
                        j1 -= 1

calculate_probs(phrase, sys.argv[4])


# i-german j-eng
