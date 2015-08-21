__author__ = 'andrew'

from gensim import models
from fileTools import verify_filesave


def build_tfidf(corpus, writedir, filename='model.tfidf'):
    tfidf = models.TfidfModel(corpus)
    tfidf.save(os.path.join(writedir + verify_filesave(filename, writedir)))
    return tfidf

def build_lsi(corpus_transform, dictionary, writedir, filename='model.tfidf', num_topics=2):
    lsi = models.LsiModel(corpus_transform, id2word=dictionary, num_topics=num_topics)
    lsi.save(os.path.join(writedir + verify_filesave(filename, writedir)))
    return lsi[corpus_transform]

def model_transform(corpus, model):
    return model[corpus]



verify_filesave('andrew', '/home/andrew/Desktop')