#from __future__ import print_function
__author__ = 'andrew'

import nltk
import os
import time
import importCorpus
import corpusTools
import preProcess

import models
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar')

def stanfordNamedEntity(doc_list):

    entity_names = []
    for doc in doc_list:
        #entity_names.extend(sorted([x for x in st.tag(doc.split()) if x[1] != 'O'], key=lambda q: q[1]))
        entity_names.extend(st.tag(preProcess.ngram(doc, 3)))  # Need to not remove punctuation and capitalization first

    entity_names = set(entity_names)

    entity_term = [preProcess.strip_doc(entity[0]) for entity in entity_names if entity[1] != 'O']
    entity_type = [entity[1] for entity in entity_names if entity[1] != 'O']
    entity_dict = dict(zip(entity_term, entity_type))


    '''
    for i in range(list1):
        entity_dict = dict[list1[i] = list2[i]]

    entity_names = dict(sorted([x for x in set(entity_names) if x[1] != 'O'], key=lambda q: q[1]))

    print entity_names
    stripped_entities = [preProcess.strip_doc(entity[0]) for entity in entity_names]
    '''
    importCorpus.save_obj(entity_dict, 'NE_dict_test.dict')
    return entity_dict


def main():


    doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/', doc_list_fn='doc_list_test.list',
                                                           doc_dict_fn='doc_dict_test.dict', file_dict_fn='file_dict_test.dict')
    entity_dict = stanfordNamedEntity(doc_list)
    print entity_dict


    #load NER dictionary
    print 'loading NER dictionary\n'
    entity_dict = importCorpus.load_objs('obj/', 'NE_dict_test.dict')

    #build corpus from dictionary
    print 'building and saving corpus\n'
    print([entity_dict.keys()])
    ner_corpus = corpusTools.build_corpus_from_dict([entity_dict.keys()], 'corpus_dict/dictionary_test.dict', corpus_filename='ner_corpus_test.mm')

    '''
    #load models
    print 'loading models\n'
    tfidf = models.load_model('models/model_test.tfidf')

    print 'building transforms'
    #print type(entity_dict.keys)
    print(entity_dict.keys())
    corpus_tfidf = models.model_transform(entity_dict.keys(), tfidf)

    for doc in corpus_tfidf:
        print(type(doc))


    entity_names = []
    for doc in doc_list:
        #entity_names.extend(sorted([x for x in st.tag(doc.split()) if x[1] != 'O'], key=lambda q: q[1]))
        entity_names.extend(st.tag(doc.split()))
    entity_names = dict(sorted([x for x in set(entity_names) if x[1] != 'O'], key=lambda q: q[1]))

    print entity_names
    stripped_entities = [preProcess.strip_doc(entity[0]) for entity in entity_names]
    '''

if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))

