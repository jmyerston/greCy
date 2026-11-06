"""Build a spaCy NER corpus from a NEReus .jsonl file.

    python scripts/build_ner_corpus.py IN.jsonl OUT.spacy

Each line becomes one doc of one sentence, with its tokens, original spacing and entity spans.
Other annotations stay missing, so that the tagger and other components skip these docs.
"""
import json
import sys

import spacy
from spacy.tokens import DocBin, Doc, Span

in_path, out_path = sys.argv[1:]
vocab = spacy.blank("grc").vocab
docs = []
with open(in_path, encoding="utf-8") as f:
    for line in f:
        example = json.loads(line)
        tokens = example["tokens"]
        doc = Doc(vocab, words=[t["text"] for t in tokens], spaces=[t["ws"] for t in tokens])
        for i, token in enumerate(doc):
            token.is_sent_start = i == 0
        spans = [Span(doc, s["token_start"], s["token_end"] + 1, label=s["label"]) for s in example["spans"]]
        doc.set_ents(spans, default="outside")
        docs.append(doc)
DocBin(docs=docs).to_disk(out_path)
print(f"{out_path}: {len(docs)} docs")
