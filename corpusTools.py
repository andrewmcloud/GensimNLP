__author__ = 'andrew'
from gensim import corpora
from fileTools import verify_filesave
import os

def __build_dict(texts, writedir='corpus_dict/', dict_filename='dictionary.dict'):
    dictionary = corpora.Dictionary(texts)
    dict_path = os.path.join(writedir + verify_filesave(writedir, dict_filename))
    dictionary.save(dict_path) #store the dictionary for future use
    return dictionary

def build_corpus(texts, writedir='corpus_dict/', corpus_filename='corpus.mm', dict_filename='dictionary.dict'):
    dictionary = __build_dict(texts, writedir, dict_filename)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpus_path = os.path.join(writedir + verify_filesave(writedir, corpus_filename))
    corpora.MmCorpus.serialize(corpus_path, corpus)
    return corpus

def build_corpus_from_dict(texts, dict_filepath, writedir='corpus_dict/', corpus_filename='corpus.mm'):
    dictionary = load_dict(dict_filepath)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpus_path = os.path.join(writedir + verify_filesave(writedir, corpus_filename))
    corpora.MmCorpus.serialize(corpus_path, corpus)
    return corpus

def load_dict(dict_filepath):
    dictionary = corpora.Dictionary.load(dict_filepath)
    return dictionary

def load_corpus(corpora_filepath):
    corpus = corpora.MmCorpus(corpora_filepath)
    return corpus