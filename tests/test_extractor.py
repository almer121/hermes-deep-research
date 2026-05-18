from deepresearch.extractor import extract_evidence
from deepresearch.searcher import OfflineCorpusSearcher, default_corpus


def test_extracts_one_evidence_per_result():
    searcher = OfflineCorpusSearcher(default_corpus())
    results = searcher.search("mixture of experts", limit=4)
    evidence = extract_evidence(results)
    assert len(evidence) == len(results)
    ids = [e.id for e in evidence]
    assert ids == sorted(set(ids), key=ids.index)


def test_evidence_has_first_sentence_claim():
    searcher = OfflineCorpusSearcher(default_corpus())
    results = searcher.search("routing collapse", limit=1)
    evidence = extract_evidence(results)
    assert evidence
    assert evidence[0].claim.endswith(".") or evidence[0].claim
