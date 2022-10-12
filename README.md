# graCy
A project for building Ancident Greek spaCy models

This spaCy project trains four ancient Greek spaCy models using the [Proiel UD corpus](https://universaldependencies.org/treebanks/grc_proiel/index.html). The four standard spaCy models (small, medium, large, and transformer) are build and packaged using the following commands:


1. python -m spacy project assets
2. python -m spacy project run all


The transformer based model uses a transformer that was trained specifically for this task (for more information on the transformer model and how it was trained see [AristoBERTo](https://huggingface.co/Jacobo/aristoBERTo)).  The spacCy transformer model outperforms ancient Greek models build with other Python nlp libraries like Stanza and Trankit. See table  below:

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 69.92     | 98.17 | 98.22 | 94.013  | 98.05 | 84.97 | 81.37 |
| Trankit | 99.91 	| 67.60     |97.86 	| 97.93 |93.03 	  | 97.50 |85.63 	|82.31  |
| Stanza  | 100	    | 51.65	    | 97.38	| 97.75	| 92.09	  | 97.42	| 80.34 |76.33  |	

The large and medium models were trained with floret word vectors.  You can find a demo of these model in my Huggingface spacy (https://huggingface.co/Jacobo)


 

