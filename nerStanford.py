#from __future__ import print_function
__author__ = 'andrew'

import os
from itertools import groupby
from nltk.tag.stanford import StanfordNERTagger
from nltk.internals import config_java
from fileTools import check_for_numbers

config_java(options='-Xmx4096m -Xms4096m')
st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar')

#st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
#                       '/usr/share/stanford-ner/stanford-ner.jar')

def stanfordNER(doc_list, min_df=0.2, max_df=.8):
    n = len(doc_list)
    entity_terms = []
    entity_tuples_temp = []
    for doc in doc_list:
        doc_entities = st.tag(doc.split())

        chunked_tuples = []
        chunked_terms = []
        for tag, chunk in groupby(doc_entities, lambda x: x[1]):
            if tag != 'O':
                chunk = ' '.join(w for (w,t) in chunk)
                chunked_tuples.append((chunk, tag))
                chunked_terms.append(chunk)

        entity_terms.append(chunked_terms)
        entity_tuples_temp.append(chunked_tuples)

    entity_terms = preProcess.min_max_df(entity_terms, n, min_df, max_df)
    entity_tuples = []
    for i, tuple_list in enumerate(entity_tuples_temp):
        entity_tuples.append([t for t in tuple_list if t[0] in entity_terms[i]])

    importCorpus.save_obj(entity_terms, 'NE_entity_terms.list')
    importCorpus.save_obj(entity_tuples, 'NE_entity_tuples.list')

    return entity_terms, entity_tuples

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

def stanfordNERStreaming(readdir='obj/', filename='doc_list.txt', min_df=0.003, max_df=0.7):
    streaming = importCorpus.StreamingDocs(os.path.join(readdir, filename))
    entity_terms = []
    entity_tuples_temp = []
    n = 0
    for doc in streaming:
        n += 1
        if n % 1 == 0:
            print 'Processing Document: {}'.format(n)
        chunked_terms, chunked_tuples = stanfordNERSingleDoc(doc)
        entity_terms.append(chunked_terms)
        entity_tuples_temp.append(chunked_tuples)

    entity_terms = preProcess.min_max_df(entity_terms, n, min_df, max_df)
    entity_tuples = []
    for i, tuple_list in enumerate(entity_tuples_temp):
        entity_tuples.append([t for t in tuple_list if t[0] in entity_terms[i]])

    importCorpus.save_obj(entity_terms, 'NE_entity_terms.list')
    importCorpus.save_obj(entity_tuples, 'NE_entity_tuples.list')

    return entity_terms, entity_tuples

########################################################################################################################

import time
import models
import importCorpus
import corpusTools
import preProcess
import docStats

def main():
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/TXT_CONVERT/DOC_TXT',
                                                           doc_list_fn='doc_list_ner.list',
                                                           doc_dict_fn='doc_dict_ner.dict',
                                                           file_dict_fn='file_dict_ner.dict')
    '''
    #doc_check, count = check_for_numbers(doc_list)
    #print(count)

    #for i, check in enumerate(doc_check):
    #    if check == False:
    #        print file_dict[i]



    for i in range(3550, 3600):
        print(doc_dict[i])
    '''
    entity_terms, entity_tuples = stanfordNERStreaming()
    print(entity_terms)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(entity_terms, corpus_filename='NE_corpus.mm', dict_filename='NE_dictionary.dict')

    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    entity_corpus = corpusTools.load_corpus('corpus_dict/NE_corpus.mm')
    entity_dictionary = corpusTools.load_dict('corpus_dict/NE_dictionary.dict')
    doc_dict = importCorpus.load_objs('obj/', 'cyber_doc_dict_n3.dict')

    #build models
    print 'building and saving models'
    entity_tfidf = models.build_tfidf(entity_corpus, filename='NE_model.tfidf')

    #load models
    print 'loading models'
    entity_tfidf = models.load_model('models/NE_model.tfidf')

    print 'building transforms'
    entity_corpus_tfidf = models.model_transform(entity_corpus, entity_tfidf)

    #getting term stats
    print 'getting term stats'
    docStats.get_entity_stats(entity_corpus, entity_corpus_tfidf, entity_dictionary, doc_dict,
                              ne_tuple_lists=entity_tuples, writedir='stats', filename='entity_TERM_STATS.csv')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))

