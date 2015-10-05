__author__ = 'andrew'

import importCorpus
import preProcess
import corpusTools
import models
import clustering
import docStats
import nerStanford
import time


#Cyber Corpus main()
def cyber_corpus(NUM_TOPICS):
    '''
    #############################################IMPORTING AND BUILDING CORPUS##########################################
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
    lsi = models.build_lsi(corpus, dictionary, num_topics=NUM_TOPICS, filename='cyberLSI_n3_c16.model')
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
    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, NUM_TOPICS)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, NUM_TOPICS)
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


def cyber_corpus_NE():
    '''
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/TXT_CONVERT',
                                                           doc_list_fn='NER_Cyber_doc_list.list',
                                                           doc_dict_fn='NER_Cyber_doc_dict.dict',
                                                           file_dict_fn='NER_Cyber_file_dict.dict')

    #building entity_terms and entity_tuples
    entity_terms, entity_tuples = nerStanford.stanfordNERStreaming(entity_terms_fn='NER_Cyber_entity_terms.list',
                                                                   entity_tuples_fn='NER_Cyber_entity_tuples.list')

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(entity_terms, corpus_filename='NER_Cyber_corpus.mm',
                             dict_filename='NER_Cyber_dictionary.dict')
    '''
    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    entity_corpus = corpusTools.load_corpus('corpus_dict/NER_Cyber_corpus.mm')
    entity_dictionary = corpusTools.load_dict('corpus_dict/NER_Cyber_dictionary.dict')
    doc_dict = importCorpus.load_objs('obj/', 'NER_Cyber_doc_dict.dict')
    entity_tuples = importCorpus.load_objs('obj/', 'NER_Cyber_entity_tuples.list')
    entity_list = importCorpus.load_objs('obj/', 'NER_Cyber_entity_terms.list')
    '''
    #build models
    print 'building and saving models'
    models.build_tfidf(entity_corpus, filename='NER_Cyber_model.tfidf')
    '''
    #load models
    print 'loading models'
    entity_tfidf = models.load_model('models/NER_Cyber_model.tfidf')

    print 'building transforms'
    entity_corpus_tfidf = models.model_transform(entity_corpus, entity_tfidf)

    #setting min max NE occurence
    entity_terms, entity_tuples = nerStanford.NE_min_max(entity_list, entity_tuples, len(doc_dict),
                                                         min_df=0.0009, max_df=.009)

    #getting term stats
    print 'getting term stats'
    #building ne_list from entity_list, can also load a file for partial document list
    ne_list = []
    [[ne_list.append(y) for y in entity] for entity in entity_terms]

    docStats.get_entity_stats(entity_corpus, entity_corpus_tfidf, entity_dictionary, doc_dict,
                              entity_tuples, ne_list=ne_list, writedir='stats',
                              filename='NE_cyber_doc_stats_3_100.csv')

#Cyber Corpus main()
def heather_corpus(NUM_TOPICS):

    #######################################IMPORTING AND BUILDING CORPUS################################################
    print 'importing corpus'
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Heather_DOCS/TXT_CONVERT',
                                                           doc_dict_fn='heather_doc_dict_n3.dict',
                                                           doc_list_fn='heather_doc_list_n3.list',
                                                           file_dict_fn='heather_file_dict_n3.dict')

    #strips corpus of punctuation and unusual unicode characters
    #tokenizes text
    print 'stripping & tokenizing text'
    texts = preProcess.tokenize_corpus(doc_list, n=3, min_df=0.072, max_df=0.7, u_start=64, u_stop=123)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(texts, corpus_filename='heatherCorpus_n3.mm', dict_filename='heatherDict_n3.dict')

    #############################################LOADING CORPUS#########################################################

    #load corpus and dictionary
    print 'loading corpus / dictionary'
    corpus = corpusTools.load_corpus('corpus_dict/heatherCorpus_n3.mm')
    dictionary = corpusTools.load_dict('corpus_dict/heatherDict_n3.dict')
    doc_dict = importCorpus.load_objs('obj/', 'heather_doc_dict_n3.dict')
    file_dict = importCorpus.load_objs('obj/', 'heather_file_dict_n3.dict')

    #build models
    print 'building and saving models'
    tfidf = models.build_tfidf(corpus, filename='heatherTFIDF_n3.model')
    lsi = models.build_lsi(corpus, dictionary, num_topics=NUM_TOPICS, filename='heatherLSI_n3.model')
    #lda = models.build_lda(corpus, dictionary, '', num_topics=5, filename='cyberLDA.model')

    #load models
    print 'loading models'
    tfidf = models.load_model('models/heatherTFIDF_n3.model')
    lsi = models.load_model('models/heatherLSI_n3.model', 'lsi')
    #lda = models.load_model('models/model.lda', 'lda')

    print 'building transforms'
    corpus_tfidf = models.model_transform(corpus, tfidf)
    corpus_lsi = models.model_transform(corpus, lsi)

    #clustering
    print 'clustering'
    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, NUM_TOPICS)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, NUM_TOPICS)
    clustering.get_docs_by_cluster(clusters, doc_dict, writedir='clusters/', filename='heather_docs_by_cluster_n3')

    #plotting clusters
    print 'plotting clusters'
    clustering.plot_2d_clusters(data_lsi, clusters, centers, filename='heather_clusters.png')
    term_list = clustering.cluster_terms(data, clusters, centers, dictionary, filename='heather_cluster_terms.txt')

    #getting term stats
    print 'getting term stats'
    docStats.get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=term_list,
                            writedir='stats', filename='heatherTERM_STATS_n3.csv')
    '''
    #print 'determining clusters\n'
    dist = clustering.determine_clusters(corpus_tfidf, num_executions=15)
    '''

def heatherNER():
    '''
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Heather_DOCS/TXT_CONVERT',
                                                           doc_dict_fn='heather_doc_dict_n3.dict',
                                                           doc_list_fn='heather_doc_list_n3.list',
                                                           file_dict_fn='heather_file_dict_n3.dict')

    #building entity_terms and entity_tuples
    entity_terms, entity_tuples_full = nerStanford.stanfordNERStreaming(min_df=.07, max_df=.7,
                                                            entity_terms_fn='heather_NE_entity_terms.list',
                                                            entity_tuples_fn='heather_NE_entity_tuples_all.list')
    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(entity_terms, corpus_filename='heatherNE_corpus.mm',
                             dict_filename='heatherNE_dictionary.dict')
    '''
    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    entity_corpus = corpusTools.load_corpus('corpus_dict/heatherNE_corpus.mm')
    entity_dictionary = corpusTools.load_dict('corpus_dict/heatherNE_dictionary.dict')
    doc_dict = importCorpus.load_objs('obj/', 'heather_doc_dict_n3.dict')
    entity_tuples = importCorpus.load_objs('obj/', 'heather_NE_entity_tuples_all.list')
    entity_list = importCorpus.load_objs('obj/', 'heather_NE_entity_terms.list')
    '''
    #build models
    print 'building and saving models'
    models.build_tfidf(entity_corpus, filename='heather_NE_model.tfidf')
    '''
    #load models
    print 'loading models'
    entity_tfidf = models.load_model('models/heather_NE_model.tfidf')

    print 'building transforms'
    entity_corpus_tfidf = models.model_transform(entity_corpus, entity_tfidf)

    #reading ne_list from file
    #with open('/home/andrew/Desktop/heather_names_list', 'r') as f:
    #    ne_list = f.read().strip().split('\n')

    #print ne_list

    #setting min max NE occurence
    entity_terms, entity_tuples = nerStanford.NE_min_max(entity_list, entity_tuples, len(doc_dict),
                                                         min_df=0.07, max_df=.3)

    #getting term stats
    print 'getting term stats'
    ne_list = []
    [[ne_list.append(y) for y in entity] for entity in entity_list]

    docStats.get_entity_stats(entity_corpus, entity_corpus_tfidf, entity_dictionary, doc_dict,
                              entity_tuples, ne_list=ne_list, writedir='stats', filename='heather_test.csv')


def main():
    #NUM_TOPICS = 4
    #cyber_corpus(NUM_TOPICS)
    #heather_corpus(NUM_TOPICS)
    #heatherNER()
    cyber_corpus_NE()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))

