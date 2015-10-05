__author__ = 'andrew'

import pickle
import os
from fileTools import verify_filesave

class StreamingDocs(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename):
            yield line

def read_docs(readdir, doc_list_fn='doc_list.list',
              doc_dict_fn='doc_dict.dict', file_dict_fn='file_dict.dict'):

    doc_list = []
    file_dict = {}
    doc_dict = {}

    #initialize doc_list && doc_dict
    for root, dirs, files in (os.walk(readdir, topdown=False)):
        for i, name in enumerate(files):
            #build full file path
            p = os.path.join(root, name)
            if not p.lower().endswith('.txt'):
                continue
            else:
                f = open(p, 'r')
                doc_list.append(f.read().replace('\n', ' '))
                file_dict[len(doc_list) - 1] = p
                doc_dict[len(doc_list) - 1] = name

    print type(doc_dict)
    save_obj(doc_list, doc_list_fn)
    save_obj(doc_dict, doc_dict_fn)
    save_obj(file_dict, file_dict_fn)

    #####saving for NER document streaming#####
    f = open('obj/doc_list.txt', 'w')
    f.write('\n'.join(doc_list))

    return doc_list, file_dict, doc_dict


def save_obj(obj, filename, writedir='obj/'):
    f = open(os.path.join(writedir, verify_filesave(writedir, filename)), 'w')
    pickle.dump(obj, f)


def load_objs(readdir, *filenames):
    if len(filenames) == 1:
        f = open(os.path.join(readdir, filenames[0]), 'r')
        return pickle.load(f)
    else:
        objlist = []
        for i in range(len(filenames)):
            f = open(os.path.join(readdir, filenames[i]), 'r')
            objlist.append(pickle.load(f))
        return objlist
