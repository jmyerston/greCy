# graCy
A project for building ancient Greek spaCy models

This spaCy project trains four ancient Greek spaCy models using the [Proiel UD corpus](https://universaldependencies.org/treebanks/grc_proiel/index.html). The four standard spaCy models (small, medium, large, and transformer) are build and packaged using the following commands:


1. python -m spacy project assets
2. python -m spacy project run all


The transformer based model uses a transformer that was trained specifically for this task and makes the model much smaller than the alternatives offered by Stanza and Trankit (for more information on the transformer model and how it was trained see [AristoBERTo](https://huggingface.co/Jacobo/aristoBERTo)).  The spaCy transformer model outperforms  Stanza in all tasks and Trankit in all metrics besides UAS and LAS. It is possible that with a longer training process our model could catch up with Trankit in this area. But among other advantages, the size remains importat: graCy tranformers is only 430 MB  vs.  the 1.2 GB of the Trankit model trained with XLM Roberta. See table  below:

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 70.09    | 98.20 | 98.35 | 94.26  | 98.05 | 85.12 | 81.49 |
| Trankit | 99.91 	| 67.60     |97.86 	| 97.93 |93.03 	  | 97.50 |85.63 	|82.31  |
| Stanza  | 100	    | 51.65	    | 97.38	| 97.75	| 92.09	  | 97.42	| 80.34 |76.33  |	

The medium  and  large models were trained with floret word vectors.  You can find demos of these models in my Huggingface spacy (https://huggingface.co/Jacobo)


 

