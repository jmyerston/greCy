import srsly
from spacy.lookups import Lookups
from spacy.util import registry


@registry.misc("greCy.load_lookup_table.v1")
def load_lookup_table(path: str) -> Lookups:
    data = srsly.read_json(path)
    lookups = Lookups()
    lookups.add_table("lemma_lookup", data)
    return lookups


@registry.misc("greCy.load_norm_table.v1")
def load_norm_table(path: str) -> Lookups:
    data = srsly.read_json(path)
    lookups = Lookups()
    lookups.add_table("lexeme_norm", data)
    return lookups


# ---------------------------------------------------------------------------------------------
# Proper-noun lemmatizer: lookup first, learned suffix rules as fallback for PROPN tokens.
# Data: data/lookup_normalization/grc_propn_lemmatizer.json (scripts/lemma_lookup/build_propn_tables.py)
# ---------------------------------------------------------------------------------------------
import unicodedata as _ud
from pathlib import Path as _Path

from spacy.language import Language
from spacy.tokens import Doc

_APOS = chr(0x2BC)


def _fold(s: str) -> str:
    """Drop diacritics and the apostrophe, keep case, fold final sigma (as canonical.fold)."""
    return "".join(c for c in _ud.normalize("NFD", s) if not _ud.combining(c)).replace("ς", "σ").replace(_APOS, "")


class PropnLemmatizer:
    """Lemmatize proper nouns that the lookup lemmatizer gets wrong.

    For each token tagged PROPN whose text is capitalised:
      * a capitalised lemma from the lookup table that differs from the form is kept;
      * a form that is itself a known name keeps it (in its canonical spelling);
      * otherwise suffix rules (conditioned on Case/Number/Gender) generate candidates on the
        diacritic-free form, and the first candidate that is a known name is used, preferring
        names whose LGPN gender matches the token;
      * failing that, a lowercase lookup lemma is capitalised (χριστός -> Χριστός for a PROPN).
    Must run after the tagger/morphologizer and the lookup lemmatizer.
    """

    def __init__(self, nlp: Language, name: str = "propn_lemmatizer"):
        self.name = name
        self.rules: dict = {}
        self.names: dict = {}

    def initialize(self, get_examples=None, *, nlp=None, data_path: str | None = None):
        if data_path:
            data = srsly.read_json(data_path)
            self.rules, self.names = data["rules"], data["names"]

    def _known(self, folded: str, gender: str):
        hit = self.names.get(folded)
        if not hit:
            return None
        name, genders = hit[0], hit[1]
        return name, (not genders or not gender or gender in genders)

    def rule_lemma(self, text: str, morph) -> str | None:
        a = _fold(text)
        key = "|".join(",".join(morph.get(k)) for k in ("Case", "Number", "Gender"))
        gender = {"Masc": "m", "Fem": "f"}.get(",".join(morph.get("Gender")), "")
        cands = []
        for j in range(len(a)):  # longest matching suffix first
            for k in (key, "||"):
                for suffix in self.rules.get(f"{k}|{a[j:]}", ()):
                    cands.append(a[:j] + suffix)
            if cands:
                break
        cands.append(a)
        fallback = None
        for c in cands:
            hit = self._known(c, gender)
            if hit:
                if hit[1]:
                    return hit[0]
                fallback = fallback or hit[0]
        return fallback

    def __call__(self, doc: Doc) -> Doc:
        if not self.names:
            return doc
        for t in doc:
            if t.pos_ != "PROPN" or not t.text[:1].isupper():
                continue
            lemma = t.lemma_
            if lemma and lemma[:1].isupper() and lemma != t.text:
                continue
            if lemma == t.text or not lemma:
                hit = self.names.get(_fold(t.text))
                if hit:
                    # a form that is itself an attested spelling stays (Αἰάκης is not Αἰακής)
                    t.lemma_ = t.text if len(hit) > 2 and t.text in hit[2] else hit[0]
                    continue
            new = self.rule_lemma(t.text, t.morph)
            if new:
                t.lemma_ = new
            elif lemma and lemma[:1].islower():
                t.lemma_ = lemma[:1].upper() + lemma[1:]
        return doc

    # serialization: the tables travel inside the packaged model
    def to_bytes(self, *, exclude=tuple()):
        return srsly.msgpack_dumps({"rules": self.rules, "names": self.names})

    def from_bytes(self, data, *, exclude=tuple()):
        d = srsly.msgpack_loads(data)
        self.rules, self.names = d["rules"], d["names"]
        return self

    def to_disk(self, path, *, exclude=tuple()):
        path = _Path(path)
        path.mkdir(parents=True, exist_ok=True)
        srsly.write_msgpack(path / "tables.msgpack", {"rules": self.rules, "names": self.names})

    def from_disk(self, path, *, exclude=tuple()):
        d = srsly.read_msgpack(_Path(path) / "tables.msgpack")
        self.rules, self.names = d["rules"], d["names"]
        return self


@Language.factory("grecy_propn_lemmatizer", requires=["token.pos", "token.morph", "token.lemma"],
                  assigns=["token.lemma"])
def make_propn_lemmatizer(nlp: Language, name: str):
    return PropnLemmatizer(nlp, name)


# ---------------------------------------------------------------------------------------------
# Morpheus lemmatizer: the main lemmatizer. For each token it picks, among the analyses of the
# pure-Python Morpheus port (ikelos), the one that best fits the predicted UPOS/morphology,
# and maps its lemma to the treebank's conventions. Tables are learned from the gold training
# docs in initialize(); the lookup lemmatizer's lemma is the tiebreaker and the fallback.
# ---------------------------------------------------------------------------------------------
import math as _math
import re as _re
from collections import Counter as _Counter, defaultdict as _dd

_DIGITS = _re.compile(r"\d+$")
# Morpheus analysis field -> UD attributes whose joint value it is compared with
_GROUPS = {
    "pos": ("UPOS", "VerbForm"),
    "tense": ("Tense", "Aspect"),
    "mood": ("Mood", "VerbForm"),
    "voice": ("Voice",),
    "gender": ("Gender",),
    "case": ("Case",),
    "number": ("Number",),
    "person": ("Person",),
    "degree": ("Degree",),
}
_SKIP_POS = {"PUNCT", "NUM", "SYM", "X"}
# used only before initialize() has learned the compatibility tables
_DEFAULT_POS = {u: {"noun", "indeclinable"} for u in ("NOUN", "ADJ", "PROPN", "PRON", "DET")}
_DEFAULT_POS.update({u: {"verb", "participle"} for u in ("VERB", "AUX")})
_DEFAULT_POS.update({u: {"indeclinable"} for u in ("ADV", "ADP", "CCONJ", "SCONJ", "PART", "INTJ")})


def _key(s: str) -> str:
    """Comparison key for lemmata: no diacritics, lowercase, final sigma folded."""
    return _fold(_ud.normalize("NFC", s)).lower()


def _ud_values(pos: str, morph) -> dict[str, str]:
    feats = morph.to_dict() if hasattr(morph, "to_dict") else dict(morph)
    feats["UPOS"] = pos
    return {g: "|".join(f"{k}={feats[k]}" for k in keys if feats.get(k)) for g, keys in _GROUPS.items()}


def _morpheus_values(a) -> dict[str, str]:
    return {g: (a.pos if g == "pos" else a.features.get(g, "")) for g in _GROUPS}


def _strip_accents(s: str) -> str:
    return _ud.normalize("NFC", "".join(c for c in _ud.normalize("NFD", s)
                                        if c not in "́̀͂"))


class MorpheusLemmatizer:
    """Lemmatize with Morpheus, disambiguated by the predicted UPOS and morphology.

    Runs after the morphologizer/tagger and the lookup lemmatizer (whose lemma is kept when
    Morpheus has no analysis, and used to break ties). The learned tables travel inside the
    packaged model; Morpheus's own data ships in the ikelos wheel.
    """

    TABLES = ("compat", "marg", "conventions", "known", "form_prior", "lemma_freq")

    def __init__(self, nlp: Language, name: str = "morpheus_lemmatizer", *,
                 min_convention_forms: int = 3, use_lookup_tiebreak: bool = True,
                 lookup_weight: float = 2.0, prior_weight: float = 1.0, trust_seen_lookup: bool = True):
        self.name = name
        self.trust_seen_lookup = trust_seen_lookup
        self.min_convention_forms = min_convention_forms
        self.use_lookup_tiebreak = use_lookup_tiebreak
        self.lookup_weight = lookup_weight
        self.prior_weight = prior_weight
        self.compat: dict = {}       # group -> morpheus value -> ud value -> count
        self.marg: dict = {}         # group -> ud value -> count
        self.conventions: dict = {}  # Morpheus lemma -> treebank lemma (εἶπον -> λέγω)
        self.known: dict = {}        # _key(lemma) -> spelling, for unambiguous keys only
        self.form_prior: dict = {}   # form and form\tUPOS -> {lemma: count} (training data)
        self.lemma_freq: dict = {}   # lemma -> count (training data)
        self._analyze = None

    # ------------------------------------------------------------------ morpheus access
    def analyses(self, text: str):
        if self._analyze is None:
            try:
                from ikelos import analyze
            except ImportError as e:  # pragma: no cover
                raise ImportError("grecy_morpheus_lemmatizer needs ikelos: pip install ikelos") from e
            self._analyze = analyze
        return self._analyze(text)

    def _respell(self, lemma: str) -> str:
        if lemma in self.lemma_freq:
            return lemma
        return self.known.get(_key(lemma), lemma)

    def _join(self, lemma: str, fallback: str) -> str | None:
        """'σύν-λέγω' -> 'συλλέγω' if the joined form matches a known lemma (or the fallback)."""
        *prefixes, verb = lemma.split("-")
        joined = "".join(_strip_accents(p) for p in prefixes) + verb
        k = _key(joined)
        if fallback and _key(fallback) == k:
            return fallback
        if k in self.known:
            return self.known[k]
        # sound changes are not modelled: accept the fallback when it ends with the verb
        if fallback and _key(fallback).endswith(_key(verb)[1:]) and _key(fallback)[:2] == _key(prefixes[0])[:2]:
            return fallback
        return None

    def normalize(self, raw: str, fallback: str = "") -> str | None:
        lemma = _DIGITS.sub("", _ud.normalize("NFC", raw))
        if lemma.endswith("-πλ"):
            lemma = lemma[:-3]
        if "-" in lemma:
            lemma = self._join(lemma, fallback)
            if lemma is None:
                return None
        lemma = self.conventions.get(lemma, lemma)
        return self._respell(lemma)

    # ------------------------------------------------------------------ scoring
    def _logp(self, group: str, mval: str, uval: str) -> float:
        row = self.compat.get(group, {}).get(mval)
        marg = self.marg.get(group, {})
        n_all = sum(marg.values()) if marg else 0
        p_u = (marg.get(uval, 0) + 0.5) / (n_all + 0.5 * (len(marg) + 1))
        if not row:
            return _math.log(p_u)
        return _math.log((row.get(uval, 0) + p_u) / (sum(row.values()) + 1.0))

    def _score_analysis(self, a, uvals: dict[str, str]) -> float:
        mvals = _morpheus_values(a)
        return sum(self._logp(g, mvals[g], uvals[g]) for g in _GROUPS)

    def choose(self, text: str, pos: str, morph, current: str) -> str | None:
        anals = self.analyses(text)
        if not anals:
            return None
        uvals = _ud_values(pos, morph)
        cur_key = _key(current) if current else None
        best: dict[str, float] = {}
        for a in anals:
            lemma = self.normalize(a.lemma, current)
            if lemma is None:
                continue
            if cur_key and _key(lemma) == cur_key:
                lemma = current  # same lemma: keep the table's spelling (μιμνῄσκω, Ὅμηρος)
            s = self._score_analysis(a, uvals) if self.compat else float(a.pos in _DEFAULT_POS.get(pos, ()))
            if s > best.get(lemma, -_math.inf):
                best[lemma] = s
        if not best:
            return None
        prior = (self.form_prior.get(f"{text}\t{uvals['pos']}") or self.form_prior.get(text)
                 or self.form_prior.get(text.lower()) or {})
        if current and current not in best and self.trust_seen_lookup and prior:
            # a form seen in training whose table lemma Morpheus does not know: a treebank
            # convention (μᾶλλον -> μάλα, εἰπεῖν -> λέγω), keep the table
            return None
        n_prior = sum(prior.values())

        def total(lemma):
            s = best[lemma]
            if self.use_lookup_tiebreak and current and lemma == current:
                s += self.lookup_weight
            if n_prior:
                s += self.prior_weight * _math.log((prior.get(lemma, 0) + 0.1) / (n_prior + 0.1))
            return (s, self.lemma_freq.get(lemma, 0))

        return max(best, key=total)  # dict order = Morpheus order on full ties

    def __call__(self, doc: Doc) -> Doc:
        for t in doc:
            if t.pos_ in _SKIP_POS or not any(c.isalpha() for c in t.text):
                continue
            new = self.choose(t.text, t.pos_, t.morph, t.lemma_)
            if new:
                t.lemma_ = new
        return doc

    # ------------------------------------------------------------------ training
    def initialize(self, get_examples=None, *, nlp=None, lookups=None):
        """Learn the tables from the gold docs of the training corpus (``get_examples``).

        Known lemma spellings also come from the lookup lemmatizer's table, when the pipeline has
        one (``nlp.get_pipe("lemmatizer")``) or one is passed as ``lookups``.
        """
        if get_examples is None:
            return
        tokens = []
        for eg in get_examples():
            for t in eg.reference:
                if t.lemma_ and t.pos_ not in _SKIP_POS and any(c.isalpha() for c in t.text):
                    tokens.append((_ud.normalize("NFC", t.text), _ud.normalize("NFC", t.lemma_),
                                   _ud_values(t.pos_, t.morph)))
        lemma_freq = _Counter(g for _, g, _ in tokens)
        form_prior: dict = _dd(_Counter)
        for w, g, uvals in tokens:
            form_prior[w][g] += 1
            form_prior[f"{w}\t{uvals['pos']}"][g] += 1  # same form, same UPOS/VerbForm
        self.lemma_freq = dict(lemma_freq)
        self.form_prior = {w: dict(c) for w, c in form_prior.items()}

        # known spellings: training lemmata first, then the lookup table's lemmata
        spellings: dict = _dd(_Counter)
        for g, c in lemma_freq.items():
            spellings[_key(g)][g] += c * 1000
        table = None
        if lookups is not None:
            table = lookups.get_table("lemma_lookup")
        elif nlp is not None and "lemmatizer" in nlp.pipe_names:
            lk = getattr(nlp.get_pipe("lemmatizer"), "lookups", None)
            if lk is not None and lk.has_table("lemma_lookup"):
                table = lk.get_table("lemma_lookup")
        if table is not None:
            for v in set(table.values()):
                spellings[_key(v)][v] += 1
        self.known = {}
        for k, c in spellings.items():
            (top, n1), *rest = c.most_common(2)
            if not rest or n1 >= 1000 > rest[0][1] or n1 > 10 * rest[0][1]:
                self.known[k] = top

        # conventions: Morpheus lemma -> gold lemma over >= min_convention_forms distinct forms
        types = {(w, g) for w, g, _ in tokens}
        cache = {}
        pairs: dict = _dd(set)
        self_forms: _Counter = _Counter()
        self.conventions = {}
        for w, g in types:
            if w not in cache:
                cache[w] = self.analyses(w)
            lemmata = {x for x in (self.normalize(a.lemma, g) for a in cache[w]) if x}
            if not lemmata or _key(g) in {_key(x) for x in lemmata}:
                for x in lemmata:
                    self_forms[x] += _key(x) == _key(g)
                continue
            for x in lemmata:
                pairs[(x, g)].add(w)
        best_conv: dict = {}
        for (x, g), ws in pairs.items():
            if len(ws) >= self.min_convention_forms and len(ws) > self_forms[x]:
                if len(ws) > len(pairs.get((x, best_conv.get(x)), ())):
                    best_conv[x] = g
        self.conventions = best_conv

        # compatibility counts from the analyses whose lemma is the gold lemma
        compat = {g: _dd(_Counter) for g in _GROUPS}
        marg = {g: _Counter() for g in _GROUPS}
        for w, g, uvals in tokens:
            good = [a for a in cache[w] if (lambda x: x and _key(x) == _key(g))(self.normalize(a.lemma, g))]
            for grp in _GROUPS:
                marg[grp][uvals[grp]] += 1
            if not good:
                continue
            wt = 1.0 / len(good)
            for a in good:
                mv = _morpheus_values(a)
                for grp in _GROUPS:
                    compat[grp][mv[grp]][uvals[grp]] += wt
        self.compat = {g: {m: dict(c) for m, c in rows.items()} for g, rows in compat.items()}
        self.marg = {g: dict(c) for g, c in marg.items()}

    # ------------------------------------------------------------------ serialization
    def _state(self):
        return {k: getattr(self, k) for k in self.TABLES}

    def _load(self, d):
        for k in self.TABLES:
            setattr(self, k, d.get(k, {}))
        return self

    def to_bytes(self, *, exclude=tuple()):
        return srsly.msgpack_dumps(self._state())

    def from_bytes(self, data, *, exclude=tuple()):
        return self._load(srsly.msgpack_loads(data))

    def to_disk(self, path, *, exclude=tuple()):
        path = _Path(path)
        path.mkdir(parents=True, exist_ok=True)
        srsly.write_msgpack(path / "tables.msgpack", self._state())

    def from_disk(self, path, *, exclude=tuple()):
        return self._load(srsly.read_msgpack(_Path(path) / "tables.msgpack"))


@Language.factory("grecy_morpheus_lemmatizer", requires=["token.pos", "token.morph"],
                  assigns=["token.lemma"],
                  default_config={"min_convention_forms": 3, "use_lookup_tiebreak": True,
                                  "lookup_weight": 2.0, "prior_weight": 1.0, "trust_seen_lookup": True})
def make_morpheus_lemmatizer(nlp: Language, name: str, min_convention_forms: int,
                             use_lookup_tiebreak: bool, lookup_weight: float, prior_weight: float,
                             trust_seen_lookup: bool):
    return MorpheusLemmatizer(nlp, name, min_convention_forms=min_convention_forms,
                              use_lookup_tiebreak=use_lookup_tiebreak, lookup_weight=lookup_weight,
                              prior_weight=prior_weight, trust_seen_lookup=trust_seen_lookup)
