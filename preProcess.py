#remove common words and tokenize

from stopwords import stopwords
from collections import defaultdict
import string

def tokenize_corpus(documents, min_df=0.1, max_df=0.9):

    texts = [[word for word in document.lower().strip().split() if word not in stopwords]
             for document in documents]

    frequency = defaultdict(int)

    for text in texts:
        set_list = []
        for token in text:
            if token not in set_list:
                set_list.append(token)
                frequency[token] += 1

    n = len(documents)
    max_n = int(round(max_df * n))
    min_n = int(round(min_df * n))

    returnlist = []
    for text in texts:
        temp = []
        for token in text:
            if min_n < frequency[token] < max_n:
                temp.append(token)
        returnlist.append(temp)

    return returnlist

def tokenize_doc(document):
    return [word for word in document.lower().strip().split() if word not in stopwords]


def strip_unicode(s):
    """Strips all unicode characters greater than 127
    :param:
        s:
            description: string
            type: string
    :returns:
        string:
        description: string with all unicode above 127 stripped
        type: string
    """
    string = ''
    for c in s:
        if (64 < ord(c) < 123) or ord(c) == 32:
            string += c

    return string


def strip_docs(documents, unicode=True):

    stripped_docs = []
    for doc in documents:
        # print doc
        stripped_doc = doc.lower().translate(None, string.punctuation)
        #remove unicode
        if unicode:
            stripped_doc = strip_unicode(stripped_doc)
        stripped_docs.append(stripped_doc)
        # print stripped_doc

    return stripped_docs
