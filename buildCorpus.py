__author__ = 'andrew'

import os
def read_docs(readdir):

    doc_list = []
    file_dict = {}
    doc_dict = {}

    #initialize doc_list && doc_dict
    for root, dirs, files in (os.walk(readdir, topdown=False)):
        for i, name in enumerate(files):
            #build full file path
            p = os.path.join(root, name)
            if not p.lower().endswith('.txt'): continue
            else:
                f = open(p, 'r')
                doc_list.append(f.read())
                file_dict[len(doc_list) - 1] = p
                doc_dict[len(doc_list) - 1] = name


    return doc_list, file_dict, doc_dict

