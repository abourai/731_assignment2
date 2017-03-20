import sys
import os

from collections import defaultdict


def union(align_file_f, align_file_e, align_file_final):

    align_f = read_f_alignments(align_file_f)
    align_e = read_e_alignments(align_file_e)

    #combined = align_f + align_e
    with open(align_file_final, 'wb') as final:

        for i in xrange(len(align_f)):
            sent = []
            combined = sorted(align_f[i] + align_e[i], key=lambda x: (x[1], x[0]))
            for (e, f) in combined:
                sent.append((e,f))
            sent = list(set(sent))
            sent = sorted(sent, key=lambda x: (x[1], x[0]))
            for (final_e, final_f) in sent:
               final.write(str(final_e) + '-' + str(final_f) + ' ')
            final.write('\n')

    return


def read_f_alignments(f_file):
	e_alignments = []
	f_alignments = []
	with open(f_file) as f_align:

		for line in f_align.readlines():
			f_sent = []
			e_sent = []
			pointers = line.rstrip().split()
			for pointer in pointers:
				f_sent.append((int(pointer.split('-')[0]), int(pointer.split('-')[1])))
				#e_sent.append((int(pointer.split('-')[1]), int(pointer.split('-')[0])))

			f_alignments.append(f_sent)
			#e_alignments.append(e_sent)

	return f_alignments


def read_e_alignments(e_file):
	e_alignments = []
	f_alignments = []
	with open(e_file) as e_align:

		for line in e_align.readlines():
			f_sent = []
			e_sent = []
			pointers = line.rstrip().split()
			for pointer in pointers:
				f_sent.append((int(pointer.split('-')[1]), int(pointer.split('-')[0])))
				#e_sent.append((int(pointer.split('-')[1]), int(pointer.split('-')[0])))

			f_alignments.append(f_sent)
			#e_alignments.append(e_sent)

	return f_alignments

def main(args):
    align_file_f = args[1]
    align_file_e = args[2]
    align_file_final = args[3]

    union(align_file_f, align_file_e, align_file_final)
    return


if __name__=='__main__':
    sys.exit(main(sys.argv))
