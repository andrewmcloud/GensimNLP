__author__ = 'andrew'

import importCorpus
import preProcess
import corpusTools
import models
import os
from gensim import matutils
from operator import itemgetter
from numpy import bincount as np_bincount
from fileTools import verify_filesave

def get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=None, writedir='stats', filename='term_stats.txt'):

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
    f.write('Term,Count,TF-IDF,DF,Documents\n')

    for i, word in enumerate(feature_names):
        if term_list == None:
            f.write('{},{},{},{},{}\n'.format(word, count[i].item(0), tfidf[i].item(0), docfreq[i], doc_str[i]))
        else:
            if word in term_list:
                f.write('{},{},{},{},{}\n'.format(word, count[i].item(0), tfidf[i].item(0), docfreq[i], doc_str[i]))



#TESTING
def main():

    doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/')

    #strips corpus of punctuation and unusual unicode characters
    print 'preprocessing text'
    doc_list = preProcess.strip_docs(doc_list)

    #tokenize text
    print 'tokenizing text'
    texts = preProcess.tokenize_corpus(doc_list, min_df=0.1, max_df=0.8)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(texts, filename='corpus_test.mm', dictfilename='dictionary_test.dict')

    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    corpus = corpusTools.load_corpus('corpus_dict/corpus_test.mm')
    dictionary = corpusTools.load_dict('corpus_dict/dictionary_test.dict')

    #loading doc_dict
    #print 'loading doc_dict'
    #doc_dict = importCorpus.load_objs('obj/', 'doc_dict.dict')

    print 'building and saving models'
    tfidf = models.build_tfidf(corpus, filename='model_test.tfidf')
    lsi = models.build_lsi(corpus, dictionary, filename='model_test.lsi', num_topics=3)
    lda = models.build_lda(corpus, dictionary, filename='model_test.lda', num_topics=3)

    print 'building transforms'
    corpus_tfidf = models.model_transform(corpus, tfidf)

    #get term stats
    print 'getting term stats'
    get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=['sector', 'proposed', 'radar'], filename='term_stats_test.txt')


if __name__ == '__main__':
    main()