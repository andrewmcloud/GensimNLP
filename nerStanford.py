#from __future__ import print_function
__author__ = 'andrew'


from itertools import groupby
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar')

def stanfordNamedEntity(doc_list, min_df=0.2, max_df=.8):
    n = len(doc_list)
    entity_terms = []
    entity_tuples_temp = []
    for doc in doc_list:
        doc_entities = st.tag(doc.split())

        chunked_tuple = []
        chunked_terms = []
        for tag, chunk in groupby(doc_entities, lambda x: x[1]):
            if tag != 'O':
                chunk = ' '.join(w for (w,t) in chunk)
                chunked_tuple.append((chunk, tag))
                chunked_terms.append(chunk)

        entity_terms.append(chunked_terms)
        entity_tuples_temp.append(chunked_tuple)

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
    doc_list, file_dict, doc_dict = importCorpus.read_docs('/home/andrew/Desktop/Cyber_Corpus/TXT_CONVERT',
                                                           doc_list_fn='doc_list_ner.list',
                                                           doc_dict_fn='doc_dict_ner.dict',
                                                           file_dict_fn='file_dict_ner.dict')
    entity_terms, entity_tuples = stanfordNamedEntity(doc_list, min_df=0.02, max_df=0.8)

    #build corpus and dictionary
    print 'building and saving corpus / dictionary'
    corpusTools.build_corpus(entity_terms, corpus_filename='NE_corpus_test.mm', dict_filename='NE_dictionary_test.dict')

    #loading corpus and dictionary
    print 'loading corpus and dictionary'
    entity_corpus = corpusTools.load_corpus('corpus_dict/NE_corpus_test.mm')
    entity_dictionary = corpusTools.load_dict('corpus_dict/NE_dictionary_test.dict')
    doc_dict = importCorpus.load_objs('obj/', 'cyber_doc_dict_n3.dict')

    #build models
    print 'building and saving models'
    entity_tfidf = models.build_tfidf(entity_corpus, filename='NE_model_test.tfidf')

    #load models
    print 'loading models'
    entity_tfidf = models.load_model('models/NE_model_test.tfidf')

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

