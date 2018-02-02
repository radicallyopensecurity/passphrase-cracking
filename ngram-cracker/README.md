# N-gram-based passphrase cracking

Most help can be found in `genphrases.py`. Some notes:

- Pre-trained models are in the `ngrams-*` files. You should decompress them (`xz -d`) before use.
- In the `*-min3` model, all words with a frequency lower than 2 were removed to reduce its size.

Quickstart:

    pypy genphrases.py -v ngrams-n2-lin+wiki 1 5 | hashcat -m 0 -r hashcat-rules/set1 -r hashcat-rules/set2 -r hashcat-rules/set3 YOURHASHFILE

If you want to generate your own models, use `ngrams.py` to generate them. If
needed, you can combine multiple (and weigh some higher than others) using
`combiner.py`.

