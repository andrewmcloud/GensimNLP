__author__ = 'andrew'
from pprint import pprint

def main():
    from buildCorpus import read_docs
    from pre_process import strip_docs
    from pre_process import tokenize
    from processCorpus import build_corpus

    doc_list, file_dict, doc_dict = read_docs('test_corpus/')
    doc_list = strip_docs(doc_list)

    texts = tokenize(doc_list)
    pprint(build_corpus(texts, 'corpora.mm'))

if __name__ == '__main__':
    main()

