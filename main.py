__author__ = 'andrew'

import importCorpus
import preProcess
import corpusTools
import models
import clustering
import docStats
import time

def main():
    '''
    #######################################IMPORTING AND BUILDING CORPUS################################################
    print 'importing corpus'
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/TXT_CONVERT',
                                                           doc_dict_fn='cyber_doc_dict.dict',
                                                           doc_list_fn='cyber_doc_list.list',
                                                           file_dict_fn='cyber_file_dict.dict')

    #strips corpus of punctuation and unusual unicode characters
    #tokenizes text
    print 'stripping & tokenizing text'
    texts = preProcess.tokenize_corpus(doc_list, n=3, min_df=0.003, max_df=0.7, u_start=64, u_stop=123)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(texts, corpus_filename='cyberCorpus.mm', dict_filename='cyberDict.dict')
    '''
    #############################################LOADING CORPUS#########################################################
    #load corpus and dictionary
    print 'loading corpus / dictionary'
    corpus = corpusTools.load_corpus('corpus_dict/cyberCorpus_n3.mm')
    dictionary = corpusTools.load_dict('corpus_dict/cyberDict_n3.dict')
    doc_dict = importCorpus.load_objs('obj/', 'cyber_doc_dict_n3.dict')
    file_dict = importCorpus.load_objs('obj/', 'cyber_file_dict_n3.dict')

    #build models
    print 'building and saving models'
    tfidf = models.build_tfidf(corpus, filename='cyberTFIDF_n3_c16.model')
    lsi = models.build_lsi(corpus, dictionary, num_topics=16, filename='cyberLSI_n3_c16.model')
    #lda = models.build_lda(corpus, dictionary, '', num_topics=5, filename='cyberLDA.model')

    #load models
    print 'loading models'
    tfidf = models.load_model('models/cyberTFIDF_n3_c16.model')
    lsi = models.load_model('models/cyberLSI_n3_c6.model', 'lsi')
    #lda = models.load_model('models/model.lda', 'lda')

    print 'building transforms'
    corpus_tfidf = models.model_transform(corpus, tfidf)
    corpus_lsi = models.model_transform(corpus, lsi)

    #clustering
    print 'clustering'
    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, 16)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, 16)
    clustering.get_docs_by_cluster(clusters, doc_dict, writedir='clusters/', filename='docs_by_cluster_n3_c16')

    #plotting clusters
    print 'plotting clusters'
    clustering.plot_2d_clusters(data_lsi, clusters, centers)
    term_list = clustering.cluster_terms(data, clusters, centers, dictionary)

    #getting term stats
    print 'getting term stats'
    docStats.get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=term_list,
                            writedir='stats', filename='cyberTERM_STATS_n3_c16.csv')

    #print 'determining clusters\n'
    #dist = clustering.determine_clusters(corpus_tfidf, num_executions=30)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))

