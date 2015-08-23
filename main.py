__author__ = 'andrew'
from pprint import pprint

def main():
    import importCorpus
    import preProcess
    import corpusTools
    import models
    import clustering
    import docStats


    #import corpus and store data
    #doc_list:
    #file_dict:
    #doc_dict:

    print 'importing corpus'
    #doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/TXT_CONVERT')
    doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/')
    #strips corpus of punctuation and unusual unicode characters
    print 'preprocessing text'
    doc_list = preProcess.strip_docs(doc_list)

    #tokenize text
    print 'tokenizing text'
    texts = preProcess.tokenize_corpus(doc_list, min_df=0.1, max_df=0.8)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(texts, corpus_filename='cyberCorpus.mm', dict_filename='cyberDict.dict')

    #load corpus and dictionary
    print 'loading corpus / dictionary'
    corpus = corpusTools.load_corpus('corpus_dict/cyberCorpus.mm')
    dictionary = corpusTools.load_dict('corpus_dict/cyberDict.dict')

    #build models
    print 'building and saving models'
    tfidf = models.build_tfidf(corpus, filename='cyberTFIDF.model')
    lsi = models.build_lsi(corpus, dictionary, num_topics=17, filename='cyberLSI.model')
    #lda = models.build_lda(corpus, dictionary, '', num_topics=5, filename='cyberLDA.model')

    '''
    #load models
    print 'loading models'
    tfidf = models.load_model('models/cyberTFIDF.model')
    lsi = models.load_model('models/cyberLSI.model', 'lsi')
    #lda = models.load_model('models/model.lda', 'lda')
    '''

    print 'building transforms'
    corpus_tfidf = models.model_transform(corpus, tfidf)
    corpus_lsi = models.model_transform(corpus, lsi)


    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, 12)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, 12)
    clustering.plot_2d_clusters(data_lsi, clusters, centers)
    term_list = clustering.cluster_terms(data, clusters, centers, dictionary)

    docStats.get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_dict=term_list,
                            writedir='stats', filename='cyberTERM_STATS.csv')

    #dist = clustering.determine_clusters(corpus_tfidf, num_executions=15)

if __name__ == '__main__':
    main()
