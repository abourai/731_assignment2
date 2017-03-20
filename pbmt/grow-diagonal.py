import sys
import os

from collections import defaultdict


def grow_diag(align_file_i, align_file_u, align_file_final):


    intersections = read_intersection_alignments(align_file_i)
    union = read_union_alignments(align_file_u)

    with open(align_file_final, 'wb') as final:

        neighboring = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        for i in xrange(len(intersections)):
            count = 0
            sent = []
            for (e, f) in intersections[i]:
                for neighbor in neighboring:
                    (e_new, f_new) = (e + neighbor[0], f + neighbor[1])
                    es = [x[0] for x in intersections[i]]
                    fs = [x[1] for x in intersections[i]]
                    #print (e_new, f_new)
                    #print ((e_new not in es) or (f_new not in fs))
                    #print (e_new, f_new) in union
                    if ((e_new not in es) or (f_new not in fs)) and ((e_new, f_new) not in sent) and (e_new, f_new) in union[i]:
                        count += 1
                    #    print (e_new, f_new)
                        sent.append((e_new, f_new))
            sent = sent + intersections[i]
            sent = sorted(sent, key=lambda x: (x[1], x[0]))
        #    print intersections[i]
        #    print sent
            for (final_e, final_f) in sent:
                final.write(str(final_e) + '-' + str(final_f) + ' ')
            final.write('\n')

    return


def read_intersection_alignments(i_file):
	alignments = []
	with open(i_file) as align:

		for line in align.readlines():
			sent = []
			pointers = line.rstrip().split()
			for pointer in pointers:
				sent.append((int(pointer.split('-')[0]), int(pointer.split('-')[1])))

			alignments.append(sent)

	return alignments


def read_union_alignments(u_file):
	alignments = []
	with open(u_file) as align:

		for line in align.readlines():
			sent = []
			pointers = line.rstrip().split()
			for pointer in pointers:
				sent.append((int(pointer.split('-')[0]), int(pointer.split('-')[1])))

			alignments.append(sent)

	return alignments


def main(args):
    align_file_i = args[1]
    align_file_u = args[2]
    align_file_final = args[3]

    grow_diag(align_file_i, align_file_u, align_file_final)
    return


if __name__=='__main__':
    sys.exit(main(sys.argv))
