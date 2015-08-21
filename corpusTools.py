__author__ = 'andrew'
from gensim import corpora

def __build_dict(texts, dict_filepath):
    dictionary = corpora.Dictionary(texts)
    dictionary.save(dict_filepath) #store the dictionary for future use
    return dictionary

def build_corpus(texts, corpora_filepath):
    corpus = [__build_dict(texts, 'dictionary.dict').doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(corpora_filepath, corpus)
    return corpus

def load_dict(dict_filepath):
    dictionary = corpora.Dictionary.load(dict_filepath)
    return dictionary

def load_corpus(corpora_filepath):
    corpus = corpora.MmCorpus(corpora_filepath)
    return corpus