#from __future__ import print_function
__author__ = 'andrew'

import nltk
import os
import time
import importCorpus

readdir = '/home/amcloud/Desktop/Files/Corpora/TestCorpus_domain'

class NamedEntity(object):

    def __init__(self):
        pass

    def preprocess(self, document):
        sentences = nltk.sent_tokenize(document)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        return tagged_sentences

    def extract_entity_names(self, t, entity_type):
        entity_names = []
        if hasattr(t, 'label') and t.label:
            print(t.label)

            #NE TYPE (t.label)           EXAMPLE
            #==========================================================
            #ORGANIZATION               Georgia-Pacific Corp., WHO
            #PERSON                     Eddy Bonte, President Obama
            #LOCATION                   Murray River, Mount Everest
            #DATE                       June, 2008-06-29
            #TIME                       two fifty am, 1:30 p.m.
            #MONEY                      175 million Canadian Dollars, GBP 10.40
            #PERCENT                    twenty pct, 18.75 %
            #FACILITY                   Washington Monument, Stonehenge
            #GPE                        South East Asia, Midlothian
            if t.label() == entity_type:
                #print(t.label)
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(self.extract_entity_names(child, entity_type))
        return entity_names

    def ne_chunking(self, text):
        return nltk.ne_chunk_sents(self.preprocess(text), binary=False)


def main():

    NE = NamedEntity()
    doc_list, file_dict, doc_dict = importCorpus.read_docs('test_corpus/', doc_list_fn='doc_list_test.list',
                                                           doc_dict_fn='doc_dict_test.dict', file_dict_fn='file_dict_test.dict')
    print(doc_dict[1])
    doc = doc_list[1]
    chunked_text = NE.ne_chunking(doc)
    entity_names = []
    for tree in chunked_text:
        #print tree
        entity_names.extend(NE.extract_entity_names(tree, 'LOCATION'))

    print (entity_names)


    '''
    for doc in doc_list:
        chunked_text = NE.ne_chunking(doc)
        entity_names = []
        for tree in chunked_text:
            entity_names.extend(NE.extract_entity_names(tree, 'NE'))
            if not os.path.exists(os.path.join(root, 'namedentity')):
                os.makedirs(os.path.join(root, 'namedentity'))
            with open(os.path.join(root, 'namedentity', name), 'w') as o:
                o.write('~'.join(entity_names))
                print('processing: {}'.format(os.path.join(root, name)))
            f.close()
            o.close()
    '''
if __name__ == '__main__':
    start_time = time.time()
    main()
    print ('execution time: {} seconds'.format(time.time() - start_time))
