__author__ = 'andrew'

import os
from gensim import matutils
from operator import itemgetter
from numpy import bincount as np_bincount, where
from fileTools import verify_filesave

def get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=None,
                   writedir='stats/', filename='term_stats.txt', cluster_docs_filename='cluster_docs.txt'):

    # convert to sparse arrays
    data = matutils.corpus2csc(corpus)
    data_tfidf = matutils.corpus2csc(corpus_tfidf)

    # words
    feature_names = sorted(dictionary.items(), key=itemgetter(0))
    #feature_names = [x[1] for x in feature_names]
    print feature_names

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
        f.write('Term~Cluster~Count~TF-IDF~DF~Documents\n')
        for word in term_list:
            i = feature_names.index(word[0])
            f.write('{}~{}~{}~{}~{}~{}\n'.format(word[0], word[1], count[i].item(0), tfidf[i].item(0),
                                                 docfreq[i], doc_str[i]))
    f.close()


def get_entity_stats(corpus, corpus_tfidf, dictionary, doc_dict, ne_tuple_lists, ne_list=None,
                     writedir='stats/', filename='term_stats.txt'):

    # convert to sparse arrays
    data = matutils.corpus2csc(corpus)
    data_tfidf = matutils.corpus2csc(corpus_tfidf)

    # words
    feature_names = sorted(dictionary.items(), key=itemgetter(0))
    feature_names = [x[1] for x in feature_names]

    #count
    count = data.sum(axis=1)

    #tfidf
    tfidf = data_tfidf.sum(axis=1)

    doc_str = ['' for x in range(len(feature_names))]
    for i, doc in enumerate(corpus):
        for term_tuple in doc:
            doc_str[term_tuple[0]] += ' | ' + doc_dict[i]

    # document frequency
    docfreq = np_bincount(data.indices)

    f = open(os.path.join(writedir, verify_filesave(writedir, filename)), 'w')
    if ne_list == None:
        f.write('Term~NE Type~Count~TF-IDF~DF\n')
        term_check = []

        for ne_tuple_list in ne_tuple_lists:
            for ne_tuple in ne_tuple_list:
                if ne_tuple[0] not in term_check:
                    term_check.append(ne_tuple[0])
                    i = feature_names.index(ne_tuple[0])
                    f.write('{}~{}~{}~{}~{}\n'.format(ne_tuple[0].encode('utf-8', 'ignore'), ne_tuple[1],
                                                      count[i].item(0), tfidf[i].item(0), docfreq[i]))
    else:
        f.write('Term~NE Type~Count~TF-IDF~DF~Documents\n')
        term_check = []
        for ne_tuple_list in ne_tuple_lists:
            for ne_tuple in ne_tuple_list:
                if (ne_tuple[0] in ne_list) and (ne_tuple[0] not in term_check):
                    term_check.append(ne_tuple[0])

                    i = feature_names.index(ne_tuple[0])
                    f.write('{}~{}~{}~{}~{}~{}\n'.format(ne_tuple[0].encode('utf-8', 'ignore'), ne_tuple[1],
                                                         count[i].item(0), tfidf[i].item(0), docfreq[i], doc_str[i]))