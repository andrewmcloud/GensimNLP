__author__ = 'andrew'
from pprint import pprint

def main():
    import importCorpus
    import preProcess
    import corpusTools
    import models
    import clustering
    import docStats


    print 'importing corpus'
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Heather_DOCS/TXT_CONVERT',
                                                           doc_dict_fn='heather_doc_dict.dict',
                                                           doc_list_fn='heather_doc_list.list',
                                                           file_dict_fn='heather_file_dict.dict')
    #doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/')
    #strips corpus of punctuation and unusual unicode characters
    print 'preprocessing text\n'
    doc_list = preProcess.strip_docs(doc_list)

    #tokenize text
    print 'tokenizing text\n'
    texts = preProcess.tokenize_corpus(doc_list, n=1, min_df=0.02, max_df=0.8)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary\n'
    corpusTools.build_corpus(texts, corpus_filename='heatherCorpus.mm', dict_filename='heatherDict.dict')

    #load corpus and dictionary
    print 'loading corpus / dictionary\n'
    corpus = corpusTools.load_corpus('corpus_dict/heatherCorpus.mm')
    dictionary = corpusTools.load_dict('corpus_dict/heatherDict.dict')
    doc_dict = importCorpus.load_objs('obj/', 'heather_doc_dict.dict')

    #build models
    print 'building and saving models\n'
    tfidf = models.build_tfidf(corpus, filename='heatherTFIDF.model')
    lsi = models.build_lsi(corpus, dictionary, num_topics=5, filename='heatherLSI.model')
    #lda = models.build_lda(corpus, dictionary, '', num_topics=5, filename='cyberLDA.model')


    #load models
    print 'loading models\n'
    tfidf = models.load_model('models/heatherTFIDF.model')
    lsi = models.load_model('models/heatherLSI.model', 'lsi')
    #lda = models.load_model('models/model.lda', 'lda')


    print 'building transforms\n'
    corpus_tfidf = models.model_transform(corpus, tfidf)
    corpus_lsi = models.model_transform(corpus, lsi)


    #clustering
    print 'clustering\n'
    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, 5)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, 5)

    #plotting clusters
    print 'plotting clusters\n'
    clustering.plot_2d_clusters(data_lsi, clusters, centers)
    term_list = clustering.cluster_terms(data, clusters, centers, dictionary)

    #getting term stats
    print 'getting term stats\n'
    docStats.get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=term_list,
                            writedir='stats', filename='heatherTERM_STATS.csv')

    #print 'determining clusters\n'
    #dist = clustering.determine_clusters(corpus_tfidf, num_executions=30)

if __name__ == '__main__':
    main()
