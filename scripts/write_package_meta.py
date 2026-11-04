"""Write the meta.json override that `spacy package --meta-path` merges into a greCy model's meta.

    python scripts/write_package_meta.py OUT --treebank {PROIEL,Perseus,NEReus}
        [--metrics metrics/MODEL.json] [--req REQUIREMENT ...]
        [--author NAME] [--email EMAIL] [--license LICENSE] [--url URL]

* performance: the scores of `spacy evaluate` on the held-out set (metrics/MODEL.json), replacing the
  dev scores and losses that training stores; spaCy's generated README.md shows them as "Accuracy".
* requirements: extra packages (spaCy adds spacy / spacy-transformers itself):
    - pymorpheus, not on PyPI: the wheel of its GitHub release, required by direct URL;
    - transformers, bounded for transformer models: their weights need transformers >= 4.31.
* description, sources, notes, author, email, license, url: shown in the README and on the GitHub
  release (training leaves them empty).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SOURCES = {
    "PROIEL": [{"name": "UD Ancient Greek PROIEL", "url": "https://universaldependencies.org/treebanks/grc_proiel/index.html",
                "author": "Dag Haug et al."},
               {"name": "PROIEL treebank 20180408 (punctuation)", "url": "https://github.com/proiel/proiel-treebank"}],
    "Perseus": [{"name": "UD Ancient Greek Perseus", "url": "https://universaldependencies.org/treebanks/grc_perseus/index.html",
                 "author": "Giuseppe G. A. Celano et al."}],
    "NEReus": [{"name": "NEReus", "url": "https://github.com/jmyerston/NEReus"}],
}
EVAL = {
    "PROIEL": "the UD Ancient Greek PROIEL test set as distributed with greCy (punctuation restored from the PROIEL "
              "XML, sentences joined at commas to follow the orthographic convention, lemma corrections), so the "
              "figures are not directly comparable with official UD PROIEL results",
    "Perseus": "the UD Ancient Greek Perseus test set as distributed with greCy (with greCy's lemma and POS corrections)",
    "NEReus": "the NEReus development set (there is no separate NEReus test set)",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--treebank", required=True, choices=sorted(SOURCES))
    ap.add_argument("--metrics", type=Path)
    ap.add_argument("--req", action="append", default=[])
    for k in ("author", "email", "license", "url"):
        ap.add_argument(f"--{k}")
    args = ap.parse_args()
    meta = {
        "description": f"Ancient Greek pipeline trained on {args.treebank} (greCy).",
        "sources": SOURCES[args.treebank],
        "notes": f"Accuracy measured with `spacy evaluate` on {EVAL[args.treebank]}.",
        "requirements": args.req,
    }
    meta.update({k: getattr(args, k) for k in ("author", "email", "license", "url") if getattr(args, k)})
    if args.metrics:
        scores = json.loads(args.metrics.read_text(encoding="utf-8"))
        meta["performance"] = {k: v for k, v in scores.items() if isinstance(v, (int, float))}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(meta.get('performance', {}))} scores; requirements: {'; '.join(args.req) or '-'}")


if __name__ == "__main__":
    main()
