# greCy
## Ancient Greek models for spaCy

This spaCy project trains seven ancient Greek models using the Perseus and Proiel  [Universal Dependency corpora](https://universaldependencies.org). Trained and already compiled wheel packages are already available on the [Hugging Face Hub](https://huggingface.co/Jacobo). Prior to installation, the models can be tested on my [Ancient Greek Syntax Analyzer](https://huggingface.co/spaces/Jacobo/syntax). In general the project gives priority to the Proiel training dataset as it is the corpus that produces more accurate and efficient models. 

### Installation

The models can be installed from the terminal with the commands below:

**For the small model:**

```
pip install https://huggingface.co/Jacobo/grc_proiel_sm/resolve/main/grc_proiel_sm-any-py3-none-any.whl
```
**For the medium:**

```
pip install https://huggingface.co/Jacobo/grc_proiel_md/resolve/main/grc_proiel_md-any-py3-none-any.whl
```
**For the large:**
```
pip install https://huggingface.co/Jacobo/grc_perseus_lg/resolve/main/grc_perseus_lg-any-py3-none-any.whl
```
**For the transformer based:**

```
pip install https://huggingface.co/Jacobo/grc_proiel_trf/resolve/main/grc_proiel_trf-any-py3-none-any.whl
```

### Loading

As usual, you can load any of the four models with the following Python lines:

```
import spacy
nlp = spacy.load("grc_proiel_XX")
```
Remember to replace  _XX  with the size of the model you would like to use, this means, _sm for small, _lg for large, and _trf for transformer. The _trf model is the most accurate but also the slowest.

If you would like to work with word vectors, choose the large models.  The vectors for the large models were trained with the TLG corpus using [floret](https://github.com/explosion/floret), a fork of [fastText](https://fasttext.cc/).

### Building

The four standard spaCy models (small, medium, large, and transformer) are built and packaged using the following commands:


1. python -m spacy project assets
2. python -m spacy project run all

### Performance


The Proiel_trf model uses for fine-tuning a transformer that was specifically trained to be used with spaCy and, consequently, makes the model much smaller than the alternatives offered by Python nlp libraries like Stanza and Trankit (for more information on the transformer model and how it was trained see [AristoBERTo](https://huggingface.co/Jacobo/aristoBERTo)).  The spaCy _trf model outperforms  Stanza and Trankit in most metrics and has the advantage that its size is only 662 MB vs.  the 1.2 GB of the Trankit model trained with XLM Roberta. For a comparison, see table  below:

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 71.90 | 98.50 | 98.40 | 94.10 | 96.9 | 85.90 | 82.50 |
| Trankit | 99.91 	| 67.60     |97.86 	| 97.93 |93.03 	  | 97.50 |85.63 	|82.31  |
| Stanza  | 100	    | 51.65	    | 97.38	| 97.75	| 92.09	  | 97.42	| 80.34 |76.33  |



Metrics, however, can be misleading. This becomes particularly obvious when you work with texts that are not part  of the training dataset. In addition, greCy's lemmatizers (in all sizes) exhibit lower benchmarks but have a substantially larger vocabulary than the Stanza and Trankit models because they were trained with a complemental lemma corpus derived from Giussepe G.A. Celano [lemmatized corpus](https://github.com/gcelano/LemmatizedAncientGreekXML). This means that the greCy's lemmatizers perform better than Trankit and Stanza when processing texts not included in the Perseus and Proiel datasets. 







