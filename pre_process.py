#remove common words and tokenize

from stopwords import stopwords
import string

def tokenize(documents, min_df=0.1, max_df=0.9):

    texts = [[word for word in document.lower().strip().split() if word not in stopwords]
             for document in documents]


    from collections import defaultdict
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
            print '{}: {}'.format(frequency[token], min_n)
            if frequency[token] < max_n:
                temp.append(token)
        returnlist.append(temp)


    #texts = [[token for token in text if frequency[token] > min_n]
    #         for text in texts]

    return returnlist


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
        if ord(c) <= 126:
            string += c


    return string


def strip_docs(documents):

    stripped_docs = []
    for doc in documents:
        # print doc
        # stripped_doc = strip_unicode(doc)
        stripped_doc = doc.lower().translate(None, string.punctuation)
        stripped_docs.append(stripped_doc)
        # print stripped_doc

    return stripped_docs
