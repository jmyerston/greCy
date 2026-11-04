"""Build the GitHub release notes for a greCy release from the packaged models.

    python scripts/release_notes.py VERSION OUT

A summary table of the held-out scores of every model packaged for VERSION (from its meta.json
"performance", written by scripts/write_package_meta.py), followed by the README.md that
`spacy package` generated for each model (features, label scheme, accuracy), as on spaCy's
own model releases.
"""
import json
import sys
from pathlib import Path

COLS = [("POS", "pos_acc"), ("TAG", "tag_acc"), ("MORPH", "morph_acc"), ("LEMMA", "lemma_acc"),
        ("UAS", "dep_uas"), ("LAS", "dep_las"), ("SENT F", "sents_f"), ("NER F", "ents_f")]

version, out = sys.argv[1], Path(sys.argv[2])
pkgs = sorted(p for p in Path("packages").glob(f"*-{version}") if (p / "meta.json").exists())
if not pkgs:
    raise SystemExit(f"no packages for version {version} in packages/")
metas = [(p, json.loads((p / "meta.json").read_text(encoding="utf-8"))) for p in pkgs]
used = [(h, k) for h, k in COLS if any(k in m.get("performance", {}) for _, m in metas)]
lines = [f"# greCy v{version}", "",
         "Held-out accuracy of each model (`spacy evaluate`; see each model's notes for the evaluation set).", "",
         "| Model | " + " | ".join(h for h, _ in used) + " |",
         "|---|" + "---:|" * len(used)]
for p, m in metas:
    perf = m.get("performance", {})
    cells = [f"{perf[k] * 100:.2f}" if isinstance(perf.get(k), (int, float)) else "–" for _, k in used]
    lines.append(f"| `{m['lang']}_{m['name']}` | " + " | ".join(cells) + " |")
lines += ["", "Install a model with `pip install <wheel URL from the assets below>`; the large and transformer "
          "models also install the pymorpheus wheel attached to this release.", ""]
for p, m in metas:
    lines += ["---", "", f"## {m['lang']}_{m['name']}", "", (p / "README.md").read_text(encoding="utf-8").strip(), ""]
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(metas)} models)")
