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
