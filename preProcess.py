#remove common words and tokenize

from stopwords import stopwords
from collections import defaultdict
import string

def tokenize_corpus(documents, n=1, min_df=0.1, max_df=0.9):

    #texts = [[word for word in document.lower().strip().split() if word not in stopwords]
    #         for document in documents]

    texts = [[word for word in ngram(document, n) if word not in stopwords] for document in documents]

    frequency = defaultdict(int)
    '''
    for text in texts:
        set_list = []
        for token in text:
            if token not in set_list:
                set_list.append(token)
                frequency[token] += 1
    '''

    n = len(documents)
    max_n = int(round(max_df * n))
    min_n = int(round(min_df * n))

    returnlist = []
    for text in texts:
        set_text = set(text)
        for set_token in set_text:
            frequency[set_token] += 1


    for text in texts:
        tmp = []
        for token in text:
            if min_n < frequency[token] < max_n:
                tmp.append(token)
        returnlist.append(tmp)


    '''
    returnlist = []
    for text in texts:
        temp = []
        for token in text:
            if min_n < frequency[token] < max_n:
                temp.append(token)
        returnlist.append(temp)
    '''
    return returnlist

def tokenize_doc(document):
    return [word for word in document.lower().strip().split() if word not in stopwords]


def strip_unicode(s, i, j):
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
        if (i < ord(c) < j) or ord(c) == 32:
            string += c

    return string


def strip_docs(documents, unicode=True, i=64, j=123):

    stripped_docs = []
    for doc in documents:
        # print doc
        stripped_doc = doc.lower().translate(None, string.punctuation)
        #remove unicode
        if unicode:
            stripped_doc = strip_unicode(stripped_doc, i, j)
        stripped_docs.append(stripped_doc)
        # print stripped_doc

    return stripped_docs

def ngram(input, n=1):
    output = []
    input = input.lower().strip().split()
    for i in range(1, n+1):
        for j in range(len(input)-i+1):
            output.append(' '.join(input[j:j+i]))
    return output
'''
def main():
    test_string = 'This is a Test oF the ngram method\n'
    print ngram(test_string, 3)

#testing
if __name__ == '__main__':
    main()
'''