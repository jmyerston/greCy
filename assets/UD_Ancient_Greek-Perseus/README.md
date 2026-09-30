# Summary

This Universal Dependencies Ancient Greek Treebank consists of an automatic
conversion of a selection of passages from the Ancient Greek and Latin
Dependency Treebank 2.1

# Introduction

The current UD treebank derives from texts taken from
the Ancient Greek and Latin Dependency Treebank 2.1 available at

* https://github.com/PerseusDL/treebank_data/tree/master/v2.1/Greek

The original data have been semi-automatically annotated. More precisely,
morphological annotation and lemmatization have been performed with the help of
the Morpheus morphological analyzer, while syntactic annotation has been done
manually. The following guidelines have been followed:

* http://nlp.perseus.tufts.edu/syntax/treebank/agdt/1.7/docs/guidelines.pdf
* https://github.com/PerseusDL/treebank_data/tree/master/AGDT2/guidelines

Further details can be found at:

* https://github.com/PerseusDL/treebank_data/tree/master/v2.1/Greek

The release contains parts of the following works:

| author | work |
| --- | --- |
| Aesop | Fabulae |
| Aeschylus | Agamemnon |
| Aeschylus | Eumenides |
| Aeschylus | Libation Bearers |
| Aeschylus | Prometheus Bound |
| Aeschylus | Persians |
| Aeschylus | Seven Against Thebes |
| Aeschylus | Supplian Women |
| Anonymous | Hymn to Demeter |
| Apollodorus | Library |
| Athenaeus | The Deipnosophists |
| Diodorus Siculus | Bibliotheca Historica |
| Herodotus | Histories |
| Hesiod | Shield of Heracles |
| Hesiod | Theogony |
| Hesiod | Works and Days |
| Homer | Iliad |
| Lysias | Against Pancleon |
| Lysias | Alcybiades 1 |
| Lysias | Alcybiades 2 |
| Lysias | On the Murder of Eratosthenes |
| Plutarch | Alcibiades |
| Plutarch | Lycurgus |
| Plybius | Histories |
| Pseudo-Homer | Hymn to Demeter |
| Sophocles | Ajax |
| Sophocles | Antigone |
| Sophocles | Electra |
| Sophocles | Oedipus Tyrannus |
| Sophocles | Trachinae |
| Thucydides | Histories |

# Acknowledgement

The current UD data have been converted by Giuseppe G. A. Celano.

The Ancient Greek and Latin treebank is a result of a joint effort between
Tufts University and Leipzig University (DH) under the supervision of Prof.
Gregory Crane. Current editors of the treebank are Giuseppe G. A. Celano,
Gregory Crane, and Bridget Almas.

Authors of the annotations are (in alphabetical order):

Giuseppe G. A. Celano, J. F. Gentile, Robert Gorman, Vanessa Gorman,
Jordan Hawkesworth, Yoana Ivanova, Tovah Keynton, Florin Leonte, Alex Lessie,
Daniel Lim Libatique, Meg Luthin, Francesco Mambrini, George Matthews,
Jack Mitchell, Molly Miller, Jessica Nord, Sean Stewart, Anthony D. Yates,
Polina Yordanova, and Sam Zukoff.

Further details can be found at:

* http://perseusdl.github.io/treebank_data/

# Basic statistics

Tree count:  13919
Word count:  202989
Token count: 202989
Dep. relations: 25 of which 0 language specific
POS tags: 14
Category=value feature pairs: 33

# References:

Bamman, David and Gregory Crane. 2011. The Ancient Greek and Latin Dependency
Treebanks. 2011. In Caroline Sporleder, Antal van den Bosch, Kalliopi Zervanou
(eds.), Language Technology for Cultural Heritage, 79-98.

Celano, Giuseppe G. A., Gregory Crane, and Bridget Almas. 2014.
The Ancient Greek and Latin Dependency treebank 2.0. https://github.com/PerseusDL/treebank_data

# Changelog

* 2022-11-15 v2.11
  * Fixed adverbially used nominals from advmod to obl.
  * Fixed adverbially used verbs from advmod to advcl.
  * Fixed interjections from advmod to discourse.
  * Fixed UPOS tags of copulae: from VERB to AUX.
* 2021-05-15 v2.8
  * Fixed non-projective punctuation using Udapi ud.FixPunct.
* 2018-04-15 v2.2
  * Repository renamed from UD_Ancient_Greek to UD_Ancient_Greek-Perseus.

<pre>
=== Machine-readable metadata =================================================
Data available since: UD v1.2
License: CC BY-NC-SA 2.5
Includes text: yes
Genre: fiction
Lemmas: converted from manual
UPOS: converted from manual
XPOS: manual native
Features: converted from manual
Relations: converted from manual
Contributors: Celano, Giuseppe G. A.; Zeman, Daniel
Contributing: elsewhere
Contact: celano@informatik.uni-leipzig.de
===============================================================================
</pre>
