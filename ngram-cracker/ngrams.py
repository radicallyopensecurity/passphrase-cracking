#!/usr/bin/env python3

n = 2  # n-gram, n=?
mincount = 3  # Only output grams that occurred >=mincount times
maxmemusage = 1024 * 1024 * 5  # in KiB
cleanupinterval = 5  # Check whether cleanup is needed every {cleanupinterval} seconds
reducebelow = 0.85  # When over maxmemusage, reduce until maxmemusage*reducebelow

import sys, os, time, gc

if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
    print('Usage: ngrams.py textfile | sort -n > output')
    exit(1)

def showOutput():
    for gram in ngrams:
        if ngrams[gram] >= mincount:
            print('{} {}'.format(ngrams[gram], gram))


def getmemusage():
    # Memory usage in kB
    f = open('/proc/{}/status'.format(os.getpid()))
    memusage = int(f.read().split('VmRSS:')[1].split('\n')[0][:-3].strip())
    f.close()
    return memusage


overusage = False  # Whether we're currently over our maxmemusage
ngrams = {}
ngramcount = 0
linecount = 0
gramsatlastcleanup = 0
starttime = time.time()
timesincecleanup = time.time()
for line in open(sys.argv[1]):
    words = line.strip().lower().split(' ')
    if len(words) < n:
        continue

    for i in range(0, len(words) - (n - 1)):
        nprime = n
        gram = ''
        space = ''

        while nprime > 0:
            """word = words[i + (n - nprime)]
            if len(word) == 1 and word != 'i' and word != 'a' and not word.isdigit():
                gram = ''
                break"""

            gram += space + words[i + (n - nprime)]
            space = ' '
            nprime -= 1

        if gram not in ngrams:
            ngrams[gram] = 1
        else:
            ngrams[gram] += 1

        ngramcount += 1

    linecount += 1

    if not overusage and time.time() > timesincecleanup + cleanupinterval:
        memusage = getmemusage()
        speed = int(round(ngramcount / (time.time() - starttime) / 1000))
        print('#N  Memory usage: {}MB  Avg speed: {}k grams/s  Total: {}k lines'.format(memusage / 1024, speed, linecount / 1000))

        if memusage > maxmemusage:
            print('#W Over max usage. Reducing until {}MB'.format(round(maxmemusage * reducebelow / 1024)))

            originalmemusage = memusage
            deletefrom = 1
            totalpurged = 0
            while memusage > maxmemusage * reducebelow and deletefrom < 1025:
                todel = []
                for gram in ngrams:
                    if ngrams[gram] <= deletefrom:
                        todel.append(gram)

                totalpurged += len(todel)
                for gram in todel:
                    del ngrams[gram]

                gc.collect()
                memusage = getmemusage()
                deletefrom *= 2

            print('#W Purged {}k grams <={} usages ({}k grams were processed since last cleanup).'.format(totalpurged / 1000, deletefrom - 1, (ngramcount - gramsatlastcleanup) / 1000))
            gramsatlastcleanup = ngramcount
            newmemusage = getmemusage()
            reduced = getmemusage() - originalmemusage
            print('#W Memory usage reduced by {}MB to {}MB.'.format(reduced / 1024, newmemusage / 1024))

            if newmemusage > maxmemusage:
                print("#E Still over the limit. Printing output until now and continuing, wish me luck!")
                overusage = True
                showOutput()
                print('#E End of output.')

        sys.stdout.flush()
        timesincecleanup = time.time()

showOutput()

