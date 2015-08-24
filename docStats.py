__author__ = 'andrew'

import importCorpus
import preProcess
import corpusTools
import models
import os
from gensim import matutils
from operator import itemgetter
from numpy import bincount as np_bincount, where
from fileTools import verify_filesave

def get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=None, writedir='stats/', filename='term_stats.txt'):

    # convert to sparse arrays
    data = matutils.corpus2csc(corpus)
    data_tfidf = matutils.corpus2csc(corpus_tfidf)

    # words
    feature_names = sorted(dictionary.items(), key=itemgetter(0))
    feature_names = [x[1] for x in feature_names]

    # count
    count = data.sum(axis=1)

    # tfidf
    tfidf = data_tfidf.sum(axis=1)

    # document list
    doc_inds = zip(*data.nonzero())
    doc_str = ['' for x in range(len(feature_names))]
    for term_doc in doc_inds:
        doc_str[term_doc[0]] = doc_str[term_doc[0]] + ' | ' + doc_dict[term_doc[1]]

    # document frequency
    docfreq = np_bincount(data.indices)

    f = open(os.path.join(writedir, verify_filesave(writedir, filename)), 'w')
    if term_list == None:
        f.write('Term~Count~TF-IDF~DF~Documents\n')
        for i, word in enumerate(feature_names):
            f.write('{}~{}~{}~{}~{}\n'.format(word, count[i].item(0), tfidf[i].item(0), docfreq[i], doc_str[i]))
    else:
        f.write('Term~Cluster~Count~TF-IDF~DF\n')
        for word in term_list:
            i = feature_names.index(word[0])
            f.write('{}~{}~{}~{}~{}\n'.format(word[0], word[1], count[i].item(0), tfidf[i].item(0), docfreq[i]))


def get_entity_stats(corpus, corpus_tfidf, dictionary, doc_dict, ne_tuple_lists=None, writedir='stats/', filename='term_stats.txt'):

    # convert to sparse arrays
    data = matutils.corpus2csc(corpus)
    data_tfidf = matutils.corpus2csc(corpus_tfidf)

    # words
    feature_names = sorted(dictionary.items(), key=itemgetter(0))
    feature_names = [x[1] for x in feature_names]

    # count
    count = data.sum(axis=1)

    # tfidf
    tfidf = data_tfidf.sum(axis=1)

    # document list
    doc_inds = zip(*data.nonzero())
    doc_str = ['' for x in range(len(feature_names))]
    for term_doc in doc_inds:
        doc_str[term_doc[0]] = doc_str[term_doc[0]] + ' | ' + doc_dict[term_doc[1]]

    # document frequency
    docfreq = np_bincount(data.indices)

    f = open(os.path.join(writedir, verify_filesave(writedir, filename)), 'w')
    if ne_tuple_lists == None:
        f.write('Term~Count~TF-IDF~DF~Documents\n')
        for i, word in enumerate(feature_names):
            f.write('{}~{}~{}~{}~{}\n'.format(word, count[i].item(0), tfidf[i].item(0), docfreq[i], doc_str[i]))
    else:
        f.write('Term~NE Type~Count~TF-IDF~DF\n')
        term_check = []
        for ne_tuple_list in ne_tuple_lists:
            for ne_tuple in ne_tuple_list:
                if ne_tuple[0] not in term_check:
                    term_check.append(ne_tuple[0])
                    i = feature_names.index(ne_tuple[0])
                    f.write('{}~{}~{}~{}~{}\n'.format(ne_tuple[0], ne_tuple[1], count[i].item(0), tfidf[i].item(0), docfreq[i]))


import clustering
#TESTING
def main():

    doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/', doc_list_fn='doc_list_test.list',
              doc_dict_fn='doc_dict_test.dict', file_dict_fn='file_dict_test.dict')

    #strips corpus of punctuation and unusual unicode characters
    #print 'preprocessing text'
    # doc_list = preProcess.strip_docs(doc_list, unicode=False)

    #tokenize text
    print 'preprocessing & tokenizing text'
    texts = preProcess.tokenize_corpus(doc_list, n=3, min_df=0.1, max_df=0.8)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(texts, corpus_filename='corpus_test.mm', dict_filename='dictionary_test.dict')

    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    corpus = corpusTools.load_corpus('corpus_dict/corpus_test.mm')
    dictionary = corpusTools.load_dict('corpus_dict/dictionary_test.dict')
    doc_dict = importCorpus.load_objs('obj/', 'doc_dict_test.dict')

    #loading doc_dict
    #print 'loading doc_dict'
    #doc_dict = importCorpus.load_objs('obj/', 'doc_dict.dict')

    print 'building and saving models'
    tfidf = models.build_tfidf(corpus, filename='model_test.tfidf')
    lsi = models.build_lsi(corpus, dictionary, filename='model_test.lsi', num_topics=3)
    lda = models.build_lda(corpus, dictionary, filename='model_test.lda', num_topics=3)

    print 'building transforms'
    corpus_tfidf = models.model_transform(corpus, tfidf)
    corpus_lsi = models.model_transform(corpus, lsi)


    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, 3)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, 3)

    clustering.plot_2d_clusters(data_lsi, clusters, centers, 'clusters/')
    term_list = clustering.cluster_terms(data, clusters, centers, dictionary, 'clusters/')


    #get term stats
    print 'getting term stats'
    get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=term_list, filename='term_stats_test2.txt')


if __name__ == '__main__':
    main()