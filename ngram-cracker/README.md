# N-gram-based passphrase cracking

Most help can be found in `genphrases.py`. Some notes:

- Pre-trained models are in the `ngrams-*` files.
- In the `*-min3` model, all words with a frequency lower than 2 were removed to reduce its size.

To be used like this:

1. Generate model(s) using `ngrams.py`
2. Optionally, combine using `combine.py`
3. Run the generator and pipe to hashcat:

    pypy genphrases.py -v ngrams-n2-lin+wiki 1 5 | hashcat -m 0 -r hashcat-rules/set1 -r hashcat-rules/set2 -r hashcat-rules/set3 YOURHASHFILE

