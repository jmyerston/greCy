# greCy
## Ancient Greek models for spaCy

This spaCy project trains four ancient Greek models using the [Proiel UD corpus](https://universaldependencies.org/treebanks/grc_proiel/index.html). Trained and already compiled wheel packages are already available on my hugginface page. They are ready for users who don't want to go through the entire training process. Prior to installation, the models can be tested on my [Ancient Greek Syntax Analyzer](https://huggingface.co/spaces/Jacobo/syntax) on the [Hugginge Face Hub](https://huggingface.co/).

### Installation

The models can be installed from the terminal with the commands below:

**For the small model:**

```
pip install https://huggingface.co/Jacobo/grc_ud_proiel_sm/resolve/main/grc_ud_proiel_sm-any-py3-none-any.whl
```
**For the medium:**

```
pip install https://huggingface.co/Jacobo/grc_ud_proiel_md/resolve/main/grc_ud_proiel_md-any-py3-none-any.whl
```
**For the large:**
```
pip install https://huggingface.co/Jacobo/grc_ud_perseus_lg/resolve/main/grc_ud_perseus_lg-any-py3-none-any.whl
```
**For the transformer based:**

```
pip install https://huggingface.co/Jacobo/grc_ud_proiel_trf/resolve/main/grc_ud_proiel_trf-any-py3-none-any.whl
```

### Loading

As usual, you can load any of the four models with the following Python lines:

```
import spacy
nlp = spacy.load("grc_ud_proiel_XX")
```
Remember to replace  _XX  with the size of the model you would like to use, this means, _sm for small, _md for medium, _lg for large, and _trf for transformer. The _trf model is the most accurate but also the slowest.

If you would like to work with word similarity, choose either the _md or _lg models.  The vectors for the medium and  large models were trained with the TLG corpus using [floret](https://github.com/explosion/floret), a fork of [fastText](https://fasttext.cc/).

### Building

The four standard spaCy models (small, medium, large, and transformer) are built and packaged using the following commands:


1. pip install -r requirements
2. python -m spacy project assets
3. python -m spacy project run all

### Performance


The _trf model uses for fine-tuning a transformer that was specifically trained to be used with spaCy and, consequently, makes the model much smaller than the alternatives offered by Python nlp libraries Stanza and Trankit (for more information on the transformer model and how it was trained see [AristoBERTo](https://huggingface.co/Jacobo/aristoBERTo)).  The spaCy _trf model outperforms  Stanza and Trankit in most metrics and has the advantage that its size is only 430 MB vs.  the 1.2 GB of the Trankit model trained with XLM Roberta. For a comparison, see table  below:

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 71.90 | 98.50 | 98.40 | 94.10 | 94.84 | 85.90 | 82.50 |
| Trankit | 99.91 	| 67.60     |97.86 	| 97.93 |93.03 	  | 97.50 |85.63 	|82.31  |
| Stanza  | 100	    | 51.65	    | 97.38	| 97.75	| 92.09	  | 97.42	| 80.34 |76.33  |











