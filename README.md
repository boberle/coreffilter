# Tools for coreference filtering

This is a companion repository of https://github.com/boberle/corefconversion.

It contains tools to filter out coreference chains in various document formats.

There is no dependencies (only stdlib), except `pytest` if you want to run the test suit.

## Jsonlines

To select only chains with mentions that contains some words, use:

```bash
python3 jsonlinesfilter.py -o out.jsonlines --include word1,word2 input.jsonlines
```

This will keep only chains with any mention containing the word `word1` OR `word2` (case sensitive), and remove all other chains.


## Author

https://boberle.com
