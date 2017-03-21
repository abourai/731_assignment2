import sys
from collections import defaultdict

with open(sys.argv[1]) as target_file:

    words = defaultdict(float)

    sentences = target_file.readlines()
    for sentence in sentences:
    #    print sentence
        for word in sentence.split():
            words[word] += 1
    #print words
    output = open(sys.argv[2], 'wb')
    for w in words.keys():
        output.write('{} {} {} {} {}\n'.format(0, 0, w, w, -0.83))

    output.write('{} {} {} {}\n'.format(0, 0, '</s>', '</s>'))
    output.write('{} {} {} {}\n'.format(0, 0, '<unk>', '<unk>'))
    output.write('0\n')
