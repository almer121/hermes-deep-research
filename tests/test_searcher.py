from deepresearch.searcher import OfflineCorpusSearcher, SearchResult, default_corpus


def test_default_corpus_is_searchable():
    searcher = OfflineCorpusSearcher(default_corpus())
    results = searcher.search("mixture of experts routing", limit=3)
    assert len(results) > 0
    assert all(isinstance(r, SearchResult) for r in results)


def test_empty_query_returns_nothing():
    searcher = OfflineCorpusSearcher(default_corpus())
    assert searcher.search("") == []


def test_score_orders_results():
    searcher = OfflineCorpusSearcher(default_corpus())
    results = searcher.search("routing collapse load balancing", limit=2)
    assert results
    assert "routing" in (results[0].title + results[0].snippet).lower()
