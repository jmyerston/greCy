"""Write the meta.json override that makes the large/transformer model wheels require pymorpheus.

    python scripts/write_meta_requirements.py VERSION WHEEL OUT

pymorpheus is not on PyPI: its wheel is uploaded to the greCy GitHub release v{VERSION} together
with the models (see `pack-pymorpheus` and `publish` in project.yml), and the models require it by
direct URL, so `pip install grc_proiel_trf-….whl` installs it automatically.
"""
import json
import sys
from pathlib import Path

version, wheel, out = sys.argv[1:4]
url = f"https://github.com/jmyerston/greCy/releases/download/v{version}/{wheel}"
Path(out).parent.mkdir(parents=True, exist_ok=True)
Path(out).write_text(json.dumps({"requirements": [f"pymorpheus @ {url}"]}, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out}: pymorpheus @ {url}")
