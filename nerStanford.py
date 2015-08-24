#from __future__ import print_function
__author__ = 'andrew'

import nltk
import os
import time
import importCorpus
import corpusTools
import preProcess
import docStats
from itertools import groupby

import models
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar')

def stanfordNamedEntity(doc_list, min_df=0.2, max_df=.8):

    n = len(doc_list)
    entity_terms = []
    entity_tuples_temp = []
    for doc in doc_list:
        #entity_names.extend(sorted([x for x in st.tag(doc.split()) if x[1] != 'O'], key=lambda q: q[1]))
        doc_entities = st.tag(doc.split()) # Need to not remove punctuation and capitalization first

        chunked_tuple = []
        chunked_terms = []
        for tag, chunk in groupby(doc_entities, lambda x: x[1]):
            # print('tag: {}\n'.format(tag))
            if tag != 'O':
                chunk = ' '.join(w for (w,t) in chunk)
                chunked_tuple.append((chunk, tag))
                chunked_terms.append(chunk)

        entity_terms.append(chunked_terms)
        entity_tuples_temp.append(chunked_tuple)
        #entity_terms.append(preProcess.min_max_df(chunked_terms, n, min_df, max_df))
        #entity_tuples.append([t for t in chunked_tuple if t[0] in chunked_terms])

    entity_terms = preProcess.min_max_df(entity_terms, n, min_df, max_df)
    entity_tuples = []
    for i, tuple_list in enumerate(entity_tuples_temp):
        entity_tuples.append([t for t in tuple_list if t[0] in entity_terms[i]])

    '''
        # entity_names.extend(st.tag(preProcess.ngram_unstripped(doc, 3)))  # Need to not remove punctuation and capitalization first

    entity_names = set(entity_names)

    # entity_term = [preProcess.strip_doc(entity[0]) for entity in entity_names if entity[1] != 'O']
    entity_type = [entity[1] for entity in entity_names if entity[1] != 'O']
    entity_term = [preProcess.strip_doc(entity[0]) for entity in entity_names]
    entity_type = [entity[1] for entity in entity_names if entity[1] != 'O']
    entity_dict = dict(zip(entity_term, entity_type))

    importCorpus.save_obj(entity_dict, 'NE_dict_test.dict')
    '''
    importCorpus.save_obj(entity_terms, 'NE_entity_terms.list')
    importCorpus.save_obj(entity_tuples, 'NE_entity_tuples.list')

    return entity_terms, entity_tuples


def main():


    doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/', doc_list_fn='doc_list_test.list',
                                                           doc_dict_fn='doc_dict_test.dict', file_dict_fn='file_dict_test.dict')
    entity_terms, entity_tuples = stanfordNamedEntity(doc_list, min_df=0.1, max_df=0.9)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(entity_terms, corpus_filename='NE_corpus_test.mm', dict_filename='NE_dictionary_test.dict')

    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    entity_corpus = corpusTools.load_corpus('corpus_dict/NE_corpus_test.mm')
    entity_dictionary = corpusTools.load_dict('corpus_dict/NE_dictionary_test.dict')
    doc_dict = importCorpus.load_objs('obj/', 'doc_dict_test.dict')

    #build models
    print 'building and saving models\n'
    entity_tfidf = models.build_tfidf(entity_corpus, filename='NE_model_test.tfidf')

    #load models
    print 'loading models\n'
    entity_tfidf = models.load_model('models/NE_model_test.tfidf')

    print 'building transforms\n'
    entity_corpus_tfidf = models.model_transform(entity_corpus, entity_tfidf)

    #getting term stats
    print 'getting term stats\n'
    print(entity_tuples)
    docStats.get_entity_stats(entity_corpus, entity_corpus_tfidf, entity_dictionary, doc_dict,
                              ne_tuple_lists=entity_tuples, writedir='stats', filename='entity_TERM_STATS.csv')

if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))

