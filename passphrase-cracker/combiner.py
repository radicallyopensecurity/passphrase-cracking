#!/usr/bin/env python3

import sys

if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
    print(
'''Usage:
    combiner.py <n> <inf|min max> [-b <bonus>] <file ...>

Combines n-gram files. Recommended to be run with pypy for speed.

Arguments:
  <n>
    The n in n-gram, e.g. 3 for trigrams.

  <inf|min max>
    Either 'inf' to process all, or a min and max. Any words falling outside
    the range will not be processed. This is useful to chop counting up into
    pieces, such that it can fit into memory.

  -b <bonus>
    A bonus to be added (summed) to each entry in the first file. For example
    if you have a really accurate source, such as previously cracked
    passphrases, and a worse but more plentiful source such as n-grams parsed
    from Wikipedia (there are many, but they're not very representative of
    real passphrases), then you can apply the bonus to the passphrase n-grams
    file to prioritize it.

  <file ...>
    One or more files. Must be in n-gram format (count + gram on each line).
''')
    exit(1)

# Used to merge cracked passphrase ngrams and wikipedia based ngrams

n = int(sys.argv[1])
sys.argv = sys.argv[1:]

bonus = 0
if sys.argv[1] == '-b':
    bonus = int(sys.argv[2])
    sys.stderr.write('Applying bonus {} to first file\n'.format(bonus))
    sys.argv = sys.argv[2:]

if sys.argv[1] != 'inf':
    processrange = (int(sys.argv[1]), int(sys.argv[2]))
    sys.argv = sys.argv[2:]
else:
    processrange = (-float('inf'), float('inf'))
    sys.argv = sys.argv[1:]

total = {}

overlap = 0
notoverlap = 0
skipped = 0

for fileno, fname in enumerate(sys.argv[1:]):
    sys.stderr.write('Processing file {}...\n'.format(fname))

    for line in open(fname):
        if line.strip() == '' or line[0] == '#' or ' ' not in line.strip():
            continue

        count, gram = line.strip().replace('!', '').replace('.', '').split(' ', 1)
        count = int(count)
        if len(gram.strip().replace('  ', ' ').split(' ')) != n:
            skipped += 1
            continue

        if count >= processrange[0] and count <= processrange[1]:
            if gram not in total:
                if fileno == 0:
                    count += bonus

                notoverlap += 1
                total[gram] = count
            else:
                overlap += 1
                total[gram] += count

if len(sys.argv[1:]) == 2:
    sys.stderr.write('{} entries matched between the two files ({} did not)\n'.format(overlap, notoverlap))

sys.stderr.write('{} entries skipped because n!={}\n'.format(skipped, n))

for gram in total:
    print('{} {}'.format(total[gram], gram))

