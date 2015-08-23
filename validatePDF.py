__author__ = 'andrew'
import enchant
from preProcess import strip_docs, tokenize_doc
from importCorpus import read_docs
import os

def validate_pdf(readdir, writedir, per_dict_words=.80, unicode=False):
    d = enchant.Dict("en_US")
    exclude = 0
    exclude_string = ''

    doc_list, file_dict, doc_dict = read_docs(readdir)
    doc_list = strip_docs(doc_list, unicode=unicode, i=0, j=127)

    for i, doc in enumerate(doc_list):
        text = tokenize_doc(doc)
        isword = 0

        for token in text:
            try:
                if d.check(token):
                    isword += 1
            except Exception as detail:
                print detail
                continue

        if float(len(text)) == 0:
            percent = 0
        else:
            percent = float(isword)/float(len(text))

        if percent < per_dict_words:
            exclude += 1
            print ('excluding: doc # {}: {}; {:.2%} dictionary words'.format(i, doc_dict[i], percent))
            exclude_string += doc_dict[i] + ','

    exclude_string = exclude_string[:-1]
    f = open(os.path.join(writedir, 'TXTexclude70.csv'), 'w')
    f.write(exclude_string)
    f.close()

    print '{} of {} documents excluded\n'.format(exclude, len(doc_list))

    return os.path.join(writedir, 'exclude.csv'), readdir
