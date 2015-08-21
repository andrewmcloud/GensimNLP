__author__ = 'andrew'
from gensim import corpora

def __build_dict(texts, dict_filepath):
    dictionary = corpora.Dictionary(texts)
    dictionary.save(dict_filepath) #store the dictionary for future use
    return dictionary

#print dictionary.token2id
def build_corpus(texts, corpora_filepath):
    corpus = [__build_dict(texts, 'dictionary.dict').doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(corpora_filepath, corpus)
    return corpus
