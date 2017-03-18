import sys
from collections import defaultdict


def make_fst(input_phrases, p_file):
    fst = defaultdict(lambda: defaultdict(int))
    p_file = open(p_file, 'wb')
    with open(input_phrases) as p:

        phrases = p.readlines()
        stateid = defaultdict(lambda: len(stateid))
        node_size = 0
        for phrase in phrases:
        #    print phrase.strip().split('\t')

            german = phrase.strip().split('\t')[0].split()
            english = phrase.strip().split('\t')[1].split()
            log_prob = phrase.strip().split('\t')[2]
            current_id  = 0
            i = 0
            while i < len(german) and german[i]+'-g' in fst[current_id]:
                current_id = fst[current_id][german[i]+'-g']
                i += 1
            while i < len(german):
                g = german[i]
                node_size +=1
                fst[current_id][g+'-g'] = node_size
                print '{} {} {} {}'.format(current_id, node_size, g, '<eps>')
                p_file.write('{} {} {} {}\n'.format(current_id, node_size, g, '<eps>'))
                current_id = node_size
                i += 1
            
            j = 0
            while j < len(english) and english[j]+'-e' in fst[current_id]:
                current_id = fst[current_id][english[j]+'-e']
                j += 1
            while j < len(english):
                e = english[j]
                node_size +=1
                fst[current_id][e+'-e'] = node_size
                print '{} {} {} {}'.format(current_id, node_size, '<eps>',e)
                p_file.write('{} {} {} {}\n'.format(current_id, node_size,'<eps>',e))
                current_id = node_size
                j += 1

            print '{} {} {} {} {}'.format(current_id, 0, '<eps>', '<eps>', log_prob)
            p_file.write('{} {} {} {} {}\n'.format(current_id, 0, '<eps>', '<eps>', log_prob))
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