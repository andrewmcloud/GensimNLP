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
    '''
    print 'importing corpus'
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/PDF/PDF_TXT')

    #strips corpus of punctuation and unusual unicode characters
    print 'preprocessing text'
    doc_list = preProcess.strip_docs(doc_list)

    #tokenize text
    print 'tokenizing text'
    texts = preProcess.tokenize_corpus(doc_list, min_df=0.1, max_df=0.8)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpus = corpusTools.build_corpus(texts, '')

    #load corpus and dictionary
    print 'loading corpus / dictionary'
    corpus = corpusTools.load_corpus('corpus.mm')
    dictionary = corpusTools.load_dict('dictionary.dict')

    #build models
    print 'building and saving models'
    tfidf = models.build_tfidf(corpus, '')
    lsi = models.build_lsi(corpus, dictionary, '', num_topics=17)
    # lda = models.build_lda(corpus, dictionary, '', num_topics=5)
    '''
    #load models
    print 'loading models'
    corpus = corpusTools.load_corpus('corpus.mm')
    dictionary = corpusTools.load_dict('dictionary.dict')
    tfidf = models.load_model('model.tfidf')
    lsi = models.load_model('model.lsi', 'lsi')
    #lda = models.load_model('model.lda', 'lda')

    print 'building transforms'
    corpus_tfidf = models.model_transform(corpus, tfidf)
    '''
    for i, doc in enumerate(corpus_tfidf):
        print (doc_dict[i])
        print(doc)
    '''
    corpus_lsi = models.model_transform(corpus, lsi)
    '''
    for i, doc in enumerate(corpus_lsi):
        print (doc_dict[i])
        print(doc)

    for topic in lsi.print_topics(2):
        print(topic)
    '''
    #corpus_lda = models.model_transform(corpus, lda)
    '''
    for i, doc in enumerate(corpus_lda):
        print (doc_dict[i])
        print(doc)

    for topic in lda.print_topics(2):
        print(topic)

    '''
    data_lsi, clusters, centers = clustering.kmeans(corpus_lsi, 17)
    data, clusters, centers = clustering.kmeans(corpus_tfidf, 17)
    clustering.plot_2d_clusters(data_lsi, clusters, centers, '')
    term_list = clustering.cluster_terms(data, clusters, centers, dictionary, '')

    docStats.get_term_stats(corpus, corpus_tfidf, dictionary, doc_dict, term_list=term_list)

    #dist = clustering.determine_clusters(corpus_tfidf, num_executions=30)

    '''
    validate_pdf('/home/andrew/Desktop/validate_test', '/home/andrew/Desktop', per_dict_words=.75, unicode=False)
    '''
if __name__ == '__main__':
    main()

