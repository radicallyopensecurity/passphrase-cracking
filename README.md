# Passphrase Cracking

In this repository you will find all relevant files for a research project into
probabilistic passphrase cracking, done by [Luc Gommans](https://lucgommans.nl)
in January 2018, with [Radically Open Security](https://radicallyopensecurity.com),
for the study [Security & Network Engineering (SNE/OS3)](https://os3.nl) (RP1).

The final paper can be found in [paper/paper.pdf](paper/paper.pdf). Our n-gram
cracker code and trained n-gram files in [ngram-cracker/](ngram-cracker/).
Everything is available under GPLv3.

## Practical Passphrase Cracking

The conclusion of our research is that, so far, a hybrid dictionary attack is
the most effective method of cracking passphrases, as described by Hugo
Labrande in his paper (see our paper for the reference). We reproduced most of
his research and are now publishing a dictionary which can be used for the
purpose, because collecting it was quite a pain :-)

You can find the dictionary in
[rosbot-integration/dict-wikiphrases.xz.partX](rosbot-integration/). It is in
two parts because Github does not allow files >100MiB, you can reassemble and
decompress it using:

    cat dict-wikiphrases.xz.part{1,2} | xz -d > dict-wikiphrases

It is 690MiB uncompressed.

Now that you have the dictionary, you'll want to add at least our mangling
rules (and perhaps some of your own), which can be found in the same folder:
[rosbot-integration/hashcat-ruleset-X](rosbot-integration/).

Now run hashcat with the appropriate `-m` value (for example, for SHA1, use `100`):

	hashfile=your-hashes.txt
    hashcat -m 100 -r hashcat-ruleset-1 -r hashcat-ruleset-2 -r hashcat-ruleset-3 $hashfile dict-wikiphrases

With this dictionary and rulesets, it should run in under 20 minutes on a
modern system. In the LinkedIn hashdump, for example, this should crack
around 2.3 million passphrases!

