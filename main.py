__author__ = 'andrew'
from pprint import pprint

def main():
    from importCorpus import read_docs
    import preProcess
    import corpusTools
    import models
    import clustering

    doc_list, file_dict, doc_dict = read_docs('/home/andrew/Desktop/Cyber_Corpus/DOC/DOC_TXT')

    doc_list = preProcess.strip_docs(doc_list)
    texts = preProcess.tokenize_corpus(doc_list, min_df=0.1, max_df=0.8)

    corpus = corpusTools.build_corpus(texts, '')
    dictionary = corpusTools.load_dict('dictionary.dict')
    tfidf = models.build_tfidf(corpus, '')
    lsi = models.build_lsi(corpus, dictionary, '')
    lda = models.build_lda(corpus, dictionary, '')
    '''
    validate_pdf('/home/andrew/Desktop/validate_test', '/home/andrew/Desktop', per_dict_words=.75, unicode=False)
    '''
    corpus = corpusTools.load_corpus('corpus.mm')
    dictionary = corpusTools.load_dict('dictionary.dict')
    tfidf = models.load_model('model.tfidf')
    lsi = models.load_model('model.lsi', 'lsi')
    lda = models.load_model('model.lda', 'lda')

    corpus_tfidf = models.model_transform(corpus, tfidf)
    '''
    for i, doc in enumerate(corpus_tfidf):
        print (doc_dict[i])
        print(doc)
    '''
    #corpus_lsi = models.model_transform(corpus, lsi)
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

    data, clusters, centers = clustering.kmeans(corpus_tfidf, 5)
    # clustering.plot_2d_clusters(data, clusters, centers, '')
    clustering.cluster_terms(data, clusters, centers, dictionary, '')


if __name__ == '__main__':
    main()

