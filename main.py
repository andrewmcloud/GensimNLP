__author__ = 'andrew'
from pprint import pprint

def main():
    from importCorpus import read_docs
    from preProcess import strip_docs
    from preProcess import tokenize_corpus
    from corpusTools import build_corpus
    from validatePDF import validate_pdf
    '''
    doc_list, file_dict, doc_dict = read_docs('test_corpus/')
    doc_list = strip_docs(doc_list)

    texts = tokenize_corpus(doc_list, min_df=0.1, max_df=0.9)
    print texts
    build_corpus(texts, 'corpora.mm')
    '''
    validate_pdf('/home/andrew/Desktop/validate_test', '/home/andrew/Desktop', per_dict_words=.75, unicode=False)

if __name__ == '__main__':
    main()

