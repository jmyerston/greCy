# greCy
## Ancient Greek models for spaCy

greCy is a set of spaCy ancient Greek models and its installer. The models were trained using the [Perseus](https://universaldependencies.org/treebanks/grc_perseus/index.html) and  [Proiel UD](https://universaldependencies.org/treebanks/grc_proiel/index.html) corpora. 

In general, models trained with the Proiel corpus perform better in POS Tagging and Dependency Parsing, while Perseus models are better at sentence segmentation using punctuation, and Morphological Analysis. Lemmatization is similar across models because they share the same look-up table. 

### Installation

The `grecy` installer package has been deprecated. To install a model, download the corresponding wheel (`.whl`) file from the [Releases page](https://github.com/jmyerston/greCy/releases) and install it directly with pip:

* grc_perseus_sm
* grc_proiel_sm
* grc_perseus_lg
* grc_proiel_lg
* grc_perseus_trf
* grc_proiel_trf
* grc_ner_trf

For example, to install grc_proiel_sm from the [v3.8 release](https://github.com/jmyerston/greCy/releases/tag/v3.8):

``` bash
pip install https://github.com/jmyerston/greCy/releases/download/v3.8/grc_proiel_sm-3.8-py3-none-any.whl
```

or, if you already downloaded the file:

``` bash
pip install grc_proiel_sm-3.8-py3-none-any.whl
```

The suffixes after the corpus name, _sm, _lg, and _trf, indicate the size of the model which directly depends on the word embedding used for training. The smallest models end in _sm (small) and are the less accurate ones: they are good for testing and building lightweight apps. The _lg and _trf are the large and transformers models which are more accurate. The _lg were trained using fasttext word vectors in the spaCy floret version, and the _trf models were trained using a special version of BERT, pertained by ourselves with the largest available Ancient Greek corpus, namely, the TLG.  The vectors for large models were also trained with the TLG corpus.


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


1. python -m weasel assets
2. python -m weasel run all







