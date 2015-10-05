#remove common words and tokenize
from stopwords import stopwords
from collections import defaultdict
import string


def tokenize_corpus(documents, n=1, min_df=0.1, max_df=0.9, u_start=64, u_stop=123):
    #tokenize documents to appropriate n-gram token length
    texts = [[word for word in ngram(document, n, u_start=u_start, u_stop=u_stop)] for document in documents]
    n = len(documents)
    return min_max_df(texts, n, min_df, max_df)


def min_max_df(texts, n, min_df=0.1, max_df=0.9):
    if min_df == 0 and max_df == 1:
        return texts

    frequency = defaultdict(int)
    returnlist = []

    max_n = int(round(max_df * n))
    min_n = int(round(min_df * n))

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
    return returnlist


def strip_unicode(s, u_start, u_stop):
    return ''.join([c for c in s if (u_start < ord(c) < u_stop) or ord(c) == 32])


def translate_non_alphanumerics(to_translate, translate_to=None):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)


def strip_doc(document, u_start=47, u_stop=123):
    if type(document) == unicode:
        stripped_doc = translate_non_alphanumerics(document.lower())
    else:
        stripped_doc = document.lower().translate(None, string.punctuation)

    return strip_unicode(stripped_doc, u_start, u_stop).strip()


def parse_doc(document, u_start=47, u_stop=123):
    if type(document) == unicode:
        stripped_doc = translate_non_alphanumerics(document.lower())
    else:
        stripped_doc = document.lower().translate(None, string.punctuation)

    stripped_doc = strip_unicode(stripped_doc, u_start, u_stop)
    words = stripped_doc.strip().split()
    return [word for word in words if word not in stopwords]


def ngram(input, n=1, u_start=48, u_stop=123):
    output = []
    input = parse_doc(input, u_start, u_stop)
    for i in range(1, n+1):
        for j in range(len(input)-i+1):
            output.append(' '.join(input[j:j+i]))
    return output
