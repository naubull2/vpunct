# Voice Input Punctuator

+ Tries to automatically puctuate voice recognized text

## Data

+ Datasets are from babi tasks data and the intent classifier dataset
 - Simple questions V2
 - movie dialogue task
 - NLU benchmark dataset

## Requirements

+ python3
  + spacy, sanic, keras

## Howto

+ You can either tag [.!?] based on pattern rules only, otherwise use a neural network model

```
./vip -m [neural|pattern]  // defaults to pattern, in which case you won't need keras
```

## Performance

The following evaluation is performed on the movie dialogue task corpus.

+ Toal number of lines : 136771
+ Number of lines with question marks : 45122

+ Pattern Only

```
Accuracy  : 0.7358669903196561
Precision : 0.8589784517158818
Recall    : 0.23853109347989895
F1 Score  : 0.3733782002358982
```

+ NNet Only

```
TBD
```

+ Joint Model

```
TBD
```

## References

+ [babi dataset](https://research.fb.com/downloads/babi/)
+ [NLU benchmark dataset](https://github.com/snipsco/nlu-benchmark/tree/master/2017-06-custom-intent-engines)
