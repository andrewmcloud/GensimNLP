__author__ = 'andrew'

from gensim import models
from fileTools import verify_filesave
import os

def build_tfidf(corpus, writedir='models/', filename='model.tfidf'):
    tfidf = models.TfidfModel(corpus)
    tfidf_path = os.path.join(writedir + verify_filesave(writedir, filename))
    tfidf.save(tfidf_path)
    return tfidf

def build_lsi(corpus_transform, dictionary, writedir='models/', filename='model.lsi', num_topics=2):
    lsi = models.LsiModel(corpus_transform, id2word=dictionary, num_topics=num_topics)
    lsi_path = os.path.join(writedir + verify_filesave(writedir, filename))
    lsi.save(lsi_path)
    return lsi

def build_lda(corpus_transform, dictionary, writedir='models/', filename='model.lda', num_topics=2):
    lda = models.LdaModel(corpus_transform, id2word=dictionary, num_topics=num_topics)
    lda_path = os.path.join(writedir + verify_filesave(writedir, filename))
    lda.save(lda_path)
    return lda

def load_model(model_filepath, model='tfidf'):
    if model == 'tfidf':
        return models.TfidfModel.load(model_filepath)
    if model == 'lsi':
        return models.LsiModel.load(model_filepath)
    if model == 'lda':
        return models.LdaModel.load(model_filepath)

def model_transform(corpus, model):
    return model[corpus]
