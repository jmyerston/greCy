# greCy
## Ancient Greek models for spaCy

greCy is a set of spaCy ancient Greek models and its installer. The models were trained using the [Perseus](https://universaldependencies.org/treebanks/grc_perseus/index.html) and  [Proiel UD](https://universaldependencies.org/treebanks/grc_proiel/index.html) corpora. Prior to installation, the models can be tested on my [Ancient Greek Syntax Analyzer](https://huggingface.co/spaces/Jacobo/syntax) on the [Hugginge Face Hub](https://huggingface.co/), where you can also check the various performance metrics of each model.

In general, models trained with the Proiel corpus perform better in POS Tagging and Dependency Parsing, while Perseus models  are better at sentence segmentation using punctuation, and Morphological Analysis. Lemmatization is similar across models because they share the same neural lemmatizer in two variants: the most accurate lemmatizer was trained with word vectors, and the other was not The best models for lemmatization are the large (_lg) models. 

### Installation

First install the python package as usual:

``` bash
pip install -U grecy
```

Once the package is successfully installed, you can proceed any of the followings models:

* grc_perseus_sm
* grc_proiel_sm
* grc_perseus_lg
* grc_proiel_lg
* grc_perseus_trf
* grc_proiel_trf


The models can be installed from the terminal with the commands below:

```
python -m grecy install MODEL
```
where you replace MODEL by any of the model names listed above.  The suffixes after the corpus name _sm, _lg, and _trf indicate the size of the model which directly depend on the word embedding used to train the models. The smallest models end in _sm (small) and the less accurate ones: they are good for testing and building lightweight apps. The _lg and _trf are the large and transformers models which are more accurate. The _lg were trained using fasttext word vectors in the spaCy floret version, and the _trf models were using a special version of BERT, pertained by ourselves with the largest Ancient Greek corpus we could find (see more below). If you would like to work with word similarity, choose the _lg models.  The vectors for large models were trained with the TLG corpus using [floret](https://github.com/explosion/floret), a fork of [fastText](https://fasttext.cc/).


### Loading

As usual, you can load any of the four models with the following Python lines:

```
import spacy
nlp = spacy.load("grc_proiel_XX")
```
Remember to replace  _XX  with the size of the model you would like to use, this means, _sm for small, _lg for large, and _trf for transformer. The _trf model is the most accurate but also the slowest.

### Use

spaCy is a powerful NLP library with many application. The most basic of its function is the morpho-syntantic annotation of texts for further processing. A common routine is to load a model, create a doc object, and process a text:

```
import spacy
nlp = spacy.load("grc_proiel_sm")

text = "καὶ πρὶν μὲν ἐν κακοῖσι κειμένην ὅμως ἐλπίς μʼ ἀεὶ προσῆγε σωθέντος τέκνου ἀλκήν τινʼ εὑρεῖν κἀπικούρησιν δόμον"

doc = nlp(text)

for token in doc:
    print(f'{token.text}, lemma: {token.lemma_} pos:{token.pos_}')
    
```

#### The apostrophe issue

Unfortunaly, there is no consensus among the different internet projects that offer ancient Greek texts about how to represent the Ancient Greek apostrophe. Modern Greek simply uses the regular apostrophe, but ancient texts available in Perseus and Perseus under Philologic use various unicode characters for the apostrophe. Instead of the apostrophe, we find the Greek koronis, modifier letter apostrophe, and right single quotation mark. Provisionally, I have opted to use modifier letter apostrophe in the corpus  with which I trained the models. This means, that if you want the greCy models to properly handle the apostrophe you have to make sure that the Ancient Greek texts that you are processing use the modifier letter apostrophe **ʼ** (U+02BC ). Otherwise the models will fail to lemmatize and tag some words in your texts that ends with an 'apostrophe'.

### Building

I offer here the project file, I use to train the models in case you want to customize your models for your specific needs. The six standard spaCy models (small, large, and transformer) are built and packaged using the following commands:


1. pip install -r requirements
2. python -m spacy project assets
3. python -m spacy project run all

### Performance

For a general comparison, I share here the metrics of the Proiel transformer grc_proiel_trf and grc_perseys_trf.  These models use for fine-tuning a transformer that was specifically trained to be used with spaCy and, consequently, makes the model much smaller than the alternatives offered by Python nlp libraries such as Stanza and Trankit (for more information on the transformer model and how it was trained see [aristoBERTo](https://huggingface.co/Jacobo/aristoBERTo)).  The greCy's _trf models outperform Stanza and Trankit in most metrics and have the advantage that their size is only ~430 MB vs.  the 1.2 GB of the Trankit model trained with XLM Roberta.  See table  below:

#### Proiel

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 71.74 | 98.11 | 98.21 | 93.91 | 96.69 | 85.59 | 82.30 |
| Trankit | 99.91 	| 67.60     |97.86 	| 97.93 |93.03 	  | 97.50 |85.63 	|82.31  |
| Stanza  | 100	    | 51.65	    | 97.38	| 97.75	| 92.09	  | 97.42	| 80.34 |76.33  |

#### Perseus

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 99.38     | 95.83 | 95.92 | 94.79 | 97.23 | 80.93 | 75.74 |
| Trankit | 99.71 | 98.70 |93.97 	| 87.25 |91.66 	  | 88.52  |83.48 	|78.56  |
| Stanza  | 99.8	 | 98.85	| 92.54	| 85.22	| 91.06	| 88.26	| 78.75 |73.35  |

### Caveat 

Metrics, however, can be misleading. This becomes particularly obvious when you work with texts that are not part of the training and evaluation dataset. In addition, greCy's lemmatizers (in all sizes) exhibit lower benchmarks in comparison to the above mentioned nlp libraries, but they have a substantially larger vocabulary than the Stanza and Trankit models because they were trained with a complemental lemma corpus derived from Giussepe G.A. Celano [lemmatized corpus](https://github.com/gcelano/LemmatizedAncientGreekXML). This means that the greCy's lemmatizers perform better than Trankit and Stanza when processing texts not included in the Perseus and Proiel datasets. 

### Future Developments

This project was initiated as part of the [Diogenet Project](https://diogenet.ucsd.edu/), a research initiative that focuses on the automatic extraction of social relations from Ancient Greek texts. As part of this project, greCy will add first, in a non distant future,  a NER pipeline for the identification of entities; later I hope also to offer pipeline for the extraction of social relation from Greek texts. This pipeline should contribute to the study of social networks in the ancient world. 











