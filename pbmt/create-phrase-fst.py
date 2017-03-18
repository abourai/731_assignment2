import sys
from collections import defaultdict


def make_fst(input_phrases, p_file):

    p_file = open(p_file, 'wb')
    with open(input_phrases) as p:

        phrases = p.readlines()
        stateid = defaultdict(lambda: len(stateid))
        for phrase in phrases:
        #    print phrase.strip().split('\t')

            german = phrase.strip().split('\t')[0].split()
            english = phrase.strip().split('\t')[1].split()
            log_prob = phrase.strip().split('\t')[2]
            lastId = 0
            for i in xrange(len(german)):
                g = german[i]
                if g not in stateid.keys():
                    print '{} {} {} {}'.format(lastId, stateid[g], g, '<eps>')
                    p_file.write('{} {} {} {}\n'.format(lastId, stateid[g], g, '<eps>'))
                    lastId = stateid[g]
                else:
                    #print '{} {} {} {}'.format(lastId, stateid[g], g, '<eps>')
                    lastId = stateid[g]
                    continue

            for j in xrange(len(english)):
                e = english[j]
                print '{} {} {} {}'.format(lastId, stateid[e], '<eps>', e)
                p_file.write('{} {} {} {}\n'.format(lastId, stateid[e], '<eps>', e))
                lastId = stateid[e]
                #print '{} {} {} {}'.format(lastId, stateid[g], g, '<eps>')

            print '{} {} {} {} {}'.format(lastId, 0, '<eps>', '<eps>', log_prob)
            p_file.write('{} {} {} {} {}\n'.format(lastId, 0, '<eps>', '<eps>', log_prob))
        p_file.write('{} {} {} {}\n'.format(0, 0, '</s>', '</s>'))
        p_file.write('{} {} {} {}\n'.format(0, 0, '<unk>', '<unk>'))
        p_file.write('0\n')

    return


def main(args):

    input_phrases = args[1]
    p_fst_file = args[2]
    make_fst(input_phrases, p_fst_file)

    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
