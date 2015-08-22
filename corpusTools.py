__author__ = 'andrew'
from gensim import corpora
from fileTools import verify_filesave
import os

def __build_dict(texts, writedir, filename='dictionary.dict'):
    dictionary = corpora.Dictionary(texts)
    dict_path = os.path.join(writedir + verify_filesave(writedir, filename))
    dictionary.save(dict_path) #store the dictionary for future use
    return dictionary

def build_corpus(texts, writedir, filename='corpus.mm', dictfilename='dictionary.dict'):
    dictionary = __build_dict(texts, writedir, dictfilename)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpus_path = os.path.join(writedir + verify_filesave(writedir, filename))
    corpora.MmCorpus.serialize(corpus_path, corpus)
    return corpus

def load_dict(dict_filepath):
    dictionary = corpora.Dictionary.load(dict_filepath)
    return dictionary

def load_corpus(corpora_filepath):
    corpus = corpora.MmCorpus(corpora_filepath)
    return corpus