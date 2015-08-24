__author__ = 'andrew'

import pickle
import os
from fileTools import verify_filesave

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
                doc_list.append(f.read())
                file_dict[len(doc_list) - 1] = p
                doc_dict[len(doc_list) - 1] = name

    print type(doc_dict)
    save_obj(doc_list, doc_list_fn)
    save_obj(doc_dict, doc_dict_fn)
    save_obj(file_dict, file_dict_fn)

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


#save_obj, load_obj unit testing
'''
def main():
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {'d': 4, 'e': 5, 'f': 6}
    dict3 = {'g': 7, 'h': 8, 'i': 9}
    dict4 = {'j': 10, 'k': 11, 'l': 12}
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    dictlist = [dict1, dict2, dict3]

    save_obj(dict1, 'dict1.test.dict')
    save_obj(dict2, 'dict2.test.dict')
    save_obj(dict3, 'dict3.test.dict')
    save_obj(dict4, 'dict4.test.dict')
    save_obj(list1, 'list1.test.list')

    load1, load2, load3, load4 = load_objs('', 'dict1.test.dict', 'dict2.test.dict', 'dict3.test.dict', 'list1.test.list')
    print load1
    print load2
    print load3
    print load4
    load4.append(11)
    print load4
if __name__ == '__main__':
    main()
'''