__author__ = 'andrew'

from gensim import models
import os

def build_tfidf(corpus, writedir):
    tfidf = models.TfidfModel(corpus)
    tfidf.save(os.path.join(writedir + 'model.tfidf'))
    return tfidf[corpus]

def build_lsi(corpus_transform, dictionary,  num_topics=2, writedir):
    lsi = models.LsiModel(corpus_transform, id2word=dictionary, num_topics=num_topics)
    lsi.save(os.path.join(writedir + 'model.lsi'))
    return lsi[corpus_transform]

    