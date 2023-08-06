#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `textnets` package."""

import sqlite3

import pandas as pd
from textnets import Corpus, Textnet


def test_corpus(corpus):
    """Test Corpus class using small data frame."""

    assert len(corpus.documents) == 7

    noun_phrases = corpus.noun_phrases()
    assert noun_phrases.sum().n == 27
    assert set(noun_phrases.columns) == {"term", "n"}

    noun_phrases_remove = corpus.noun_phrases(remove=["moon"])
    assert noun_phrases_remove.sum().n == 23
    assert set(noun_phrases_remove.columns) == {"term", "n"}

    noun_phrases_remove = corpus.noun_phrases(normalize=True)
    assert set(noun_phrases_remove.columns) == {"term", "n"}

    tokenized = corpus.tokenized()
    assert tokenized.sum().n == 43
    assert set(tokenized.columns) == {"term", "n"}

    nostem = corpus.tokenized(stem=False)
    assert set(nostem.columns) == {"term", "n"}

    nopunct = corpus.tokenized(remove_punctuation=False)
    assert set(nopunct.columns) == {"term", "n"}

    upper = corpus.tokenized(lower=False)
    assert set(upper.columns) == {"term", "n"}

    ngrams = corpus.ngrams(3)
    assert ngrams.sum().n == 67
    assert set(ngrams.columns) == {"term", "n"}


def test_corpus_missing(testdata, recwarn):
    """Test Corpus class on series with missing data."""
    s = testdata.append(pd.Series([None], index=["Missing"]))
    corpus = Corpus(s)
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "Dropping 1 empty document(s)."
    assert len(corpus.documents) == 7


def test_corpus_czech(recwarn):
    """Test Corpus class using Czech language documents."""
    s = pd.Series(
        [
            "Holka modrooká nesedávej tam",
            "Holka modrooká nesedávej u potoka",
            "podemele tvoje oči",
            "vezme li tě bude škoda",
            "V potoce je hastrmánek",
            "V potoce je velká voda",
            "V potoce se voda točí",
            "zatahá tě za copánek",
        ]
    )
    # This raises a warning about an uninstalled language model
    corpus = Corpus(s, lang="cs")
    assert len(corpus.documents) == 8
    # This raises another warning about lacking a language model
    tokenized = corpus.tokenized()
    assert len(recwarn) == 2
    assert tokenized.sum().n > 8
    w1 = recwarn.pop(UserWarning)
    assert str(w1.message) == "Language model 'cs' is not yet installed."
    w2 = recwarn.pop(UserWarning)
    assert str(w2.message) == "Using basic 'cs' language model."


def test_corpus_df(testdata):
    df = pd.DataFrame({"headlines": testdata, "meta": list("ABCDEFG")})
    c = Corpus.from_df(df, doc_col="headlines")
    assert len(c.documents) == 7


def test_corpus_dict(testdata):
    data = testdata.to_dict()
    c = Corpus.from_dict(data)
    assert len(c.documents) == 7


def test_corpus_csv(tmpdir, testdata):
    out = tmpdir.join("corpus.csv")
    testdata.to_csv(out)
    c = Corpus.from_csv(out)
    assert len(c.documents) == 7


def test_corpus_sql(testdata):
    with sqlite3.connect(":memory:") as conn:
        testdata.to_sql("headlines", conn)
        c = Corpus.from_sql("SELECT * FROM headlines", conn)
    assert len(c.documents) == 7


def test_textnet(corpus):
    """Test Textnet class using sample data."""

    noun_phrases = corpus.noun_phrases()

    tn_np = Textnet(noun_phrases)
    assert tn_np.graph.vcount() > 0
    assert tn_np.graph.ecount() > 0
    g_np_groups = tn_np.project(node_type="doc")
    assert g_np_groups.vcount() > 0
    assert g_np_groups.ecount() > 0
    g_np_words = tn_np.project(node_type="term")
    assert g_np_words.vcount() > 0
    assert g_np_words.ecount() > 0


def test_context(corpus):
    """Test formal context creation from textnet."""

    tn = Textnet(corpus.tokenized(), sublinear=False)
    ctx = tn.context
    assert len(ctx) == 3


def test_save(tmpdir, corpus):
    """Test Textnet graph saving."""

    noun_phrases = corpus.noun_phrases()
    tn_np = Textnet(noun_phrases)
    out = tmpdir.join("graph.graphml")
    tn_np.save_graph(str(out))
    assert len(tmpdir.listdir()) == 1


def test_plot(tmpdir, corpus):
    """Test Textnet plotting."""

    noun_phrases = corpus.noun_phrases()
    tn_np = Textnet(noun_phrases)
    out = tmpdir.join("plot-0.png")
    plot = tn_np.plot(target=str(out))
    assert len(plot._objects) > 0
    assert len(tmpdir.listdir()) == 1


def test_plot_layout(tmpdir, corpus):
    """Test Textnet plotting with bipartite layout and node labels."""

    noun_phrases = corpus.noun_phrases()
    tn_np = Textnet(noun_phrases)
    out = tmpdir.join("plot-1.png")
    plot = tn_np.plot(target=str(out), bipartite_layout=True, label_nodes=True)
    assert len(plot._objects) > 0
    assert len(tmpdir.listdir()) == 1


def test_plot_projected(tmpdir, corpus):
    """Test ProjectedTextnet plotting."""

    tn = Textnet(corpus.tokenized())
    papers = tn.project(node_type="doc")
    out = tmpdir.join("plot-2.png")
    plot = papers.plot(show_clusters=True, label_nodes=True, target=str(out))
    assert len(plot._objects) > 0
    assert len(tmpdir.listdir()) == 1


def test_plot_backbone(tmpdir, corpus):
    """Test ProjectedTextnet plotting with alpha cut."""

    tn = Textnet(corpus.tokenized())
    papers = tn.project(node_type="doc")
    out = tmpdir.join("plot-3.png")
    plot = papers.plot(alpha=0.4, label_nodes=True, target=str(out))
    assert len(plot._objects) > 0
    assert len(tmpdir.listdir()) == 1


def test_plot_scaled(tmpdir, corpus):
    """Test ProjectedTextnet plotting with scaled nodes."""

    tn = Textnet(corpus.tokenized())
    papers = tn.project(node_type="doc")
    out = tmpdir.join("plot-4.png")
    plot = papers.plot(scale_nodes_by="betweenness", label_nodes=True, target=str(out))
    assert len(plot._objects) > 0
    assert len(tmpdir.listdir()) == 1


def test_plot_filtered(tmpdir, corpus):
    """Test ProjectedTextnet plotting filtered labels."""

    tn = Textnet(corpus.tokenized())
    papers = tn.project(node_type="doc")
    out = tmpdir.join("plot-5.png")
    plot = papers.plot(
        label_nodes=True,
        label_edges=True,
        node_label_filter=lambda v: v.degree() > 2,
        edge_label_filter=lambda e: e["weight"] > 0.1,
        target=str(out),
    )
    assert len(plot._objects) > 0
    assert len(tmpdir.listdir()) == 1
