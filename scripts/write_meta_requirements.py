"""Write a meta.json override with extra package requirements for `spacy package --meta-path`.

    python scripts/write_meta_requirements.py OUT REQUIREMENT [REQUIREMENT ...]

spaCy adds spacy and spacy-transformers itself. Used by `pack-pymorpheus` in project.yml for:
  * pymorpheus, which is not on PyPI: its wheel is uploaded to the greCy GitHub release together
    with the models and required by direct URL ("pymorpheus @ https://…/pymorpheus-….whl");
  * transformers, bounded for the transformer models: their weights are saved by transformers
    >= 4.31 (no `embeddings.position_ids` buffer) and do not load with older versions.
"""
import json
import sys
from pathlib import Path

out, reqs = Path(sys.argv[1]), sys.argv[2:]
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"requirements": reqs}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out}: " + "; ".join(reqs))
