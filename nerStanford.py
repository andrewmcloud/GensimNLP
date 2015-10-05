__author__ = 'andrew'

import os
from itertools import groupby
from nltk.tag.stanford import StanfordNERTagger
from nltk.internals import config_java

config_java(options='-Xmx4096m -Xms4096m')
st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar')

def stanfordNERSingleDoc(doc):
    doc_entities = st.tag(doc.split())
    chunked_tuples = []
    chunked_terms = []
    for tag, chunk in groupby(doc_entities, lambda x: x[1]):
        if tag != 'O':
            chunk = ' '.join(w for (w,t) in chunk)
            chunked_tuples.append((chunk, tag))
            chunked_terms.append(chunk)
    return chunked_terms, chunked_tuples

def stanfordNERStreaming(readdir='obj/', filename='doc_list.txt', min_df=0.003, max_df=0.7,
                         entity_terms_fn='NE_entity_terms.list',
                         entity_tuples_fn='NE_entity_tuples_all.list'):
    streaming = importCorpus.StreamingDocs(os.path.join(readdir, filename))
    entity_terms = []
    entity_tuples = []
    n = 0
    for doc in streaming:
        n += 1
        if n % 1 == 0:
            print 'Processing Document: {}'.format(n)
        chunked_terms, chunked_tuples = stanfordNERSingleDoc(doc)
        entity_terms.append(chunked_terms)
        entity_tuples.append(chunked_tuples)

    entity_terms = preProcess.min_max_df(entity_terms, n, min_df, max_df)

    importCorpus.save_obj(entity_terms, entity_terms_fn)
    importCorpus.save_obj(entity_tuples, entity_tuples_fn)

    return entity_terms, entity_tuples

################################################TESTING#################################################################

import time
import models
import importCorpus
import corpusTools
import preProcess
import docStats

def main():
    '''
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/TXT_CONVERT',
                                                           doc_list_fn='doc_list_ner_2docmin.list',
                                                           doc_dict_fn='doc_dict_ner_2docmin.dict',
                                                           file_dict_fn='file_dict_ner_2docmin.dict')

    #building entity_terms and entity_tuples
    entity_terms, entity_tuples, entity_tuples_temp = stanfordNERStreaming(min_df=.00036, max_df=.7,
                                                       entity_terms_fn='NE_entity_terms_2docmin.list',
                                                       entity_tuples_fn='NE_entity_tuples_2docmin.list')

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(entity_terms, corpus_filename='NE_corpus_2docmin.mm',
                             dict_filename='NE_dictionary_2docmin.dict')
    '''
    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    entity_corpus = corpusTools.load_corpus('corpus_dict/NE_corpus_2docmin.mm')
    entity_dictionary = corpusTools.load_dict('corpus_dict/NE_dictionary_2docmin.dict')
    doc_dict = importCorpus.load_objs('obj/', 'cyber_doc_dict_n3.dict')
    entity_tuples = importCorpus.load_objs('obj/', 'NE_entity_tuples_2docmin.list')

    #build models
    print 'building and saving models'
    models.build_tfidf(entity_corpus, filename='NE_model_2docmin.tfidf')

    #load models
    print 'loading models'
    entity_tfidf = models.load_model('models/NE_model_2docmin.tfidf')

    print 'building transforms'
    entity_corpus_tfidf = models.model_transform(entity_corpus, entity_tfidf)

    #reading ne_list from file
    with open('/home/andrew/Desktop/ne_list.txt', 'r') as f:
        ne_list = f.read().strip().split('\n')

    print ne_list

    #getting term stats
    print 'getting term stats'
    #docStats.get_entity_stats(entity_corpus, entity_corpus_tfidf, entity_dictionary, doc_dict,
    #                          entity_tuples, writedir='stats', filename='entity_TERM_STATS_2docmin.csv')

    docStats.get_entity_stats(entity_corpus, entity_corpus_tfidf, entity_dictionary, doc_dict,
                              entity_tuples, ne_list=ne_list, writedir='stats', filename='dates.csv')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))

