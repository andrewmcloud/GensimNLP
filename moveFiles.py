#from __future__ import print_function
__author__ = 'amcloud'
import os
import random
import shutil as sh

#attempt to copy from mitre1_clean/originals - return True if successful (used for error checking)
def __doc(f, dir):
    M1 = '/home/andrew/Desktop/Cyber_Corpus/DOC'
    try:
        if not os.path.exists(os.path.join(dir, f)):
            sh.copyfile(os.path.join(M1, f), os.path.join(dir, f))
        return True
    except:
        IOError()
        return False

#attempt to copy from mitre2_originals - return True if successful (used for error checking)
def __docx(f, dir):
    M1 = '/home/andrew/Desktop/Cyber_Corpus/DOCX'
    try:
        if not os.path.exists(os.path.join(dir, f)):
            sh.copyfile(os.path.join(M1, f), os.path.join(dir, f))
        return True
    except:
        IOError()
        return False

#attempt to copy from mitre3_originals - return True if successful (used for error checking)
def __pdf(f, dir):
    M1 = '/home/andrew/Desktop/Cyber_Corpus/PDF'
    try:
        if not os.path.exists(os.path.join(dir, f)):
            sh.copyfile(os.path.join(M1, f), os.path.join(dir, f))
        return True
    except:
        IOError()
        return False

#attempt to copy from mitre3_originals - return True if successful (used for error checking)
def __txt(f, dir):
    M1 = '/home/andrew/Desktop/Cyber_Corpus/TXT'
    try:
        if not os.path.exists(os.path.join(dir, f)):
            sh.copyfile(os.path.join(M1, f), os.path.join(dir, f))
        return True
    except:
        IOError()
        return False

#list of functions attempting to copy from mitre 1, 2, 3 directories
mitredocs = [__doc, __docx, __pdf]

def build_file_list(filename='clusters/docs_by_cluster_n3_c16'):
    return [line.strip().split('~') for line in open(filename)]

def random_select(percentage=.9):
    count = 0
    #Ensure DEV_DIR exists
    if not os.path.exists(OUT1):
        os.makedirs(OUT1)
    #Ensure TEST_DIR exits
    if not os.path.exists(OUT2):
        os.makedirs(OUT2)

    #Load comma separated file names into list: file_names[]
    file_names = build_file_list()

    #Randomize order of file_names[]
    sum = 0
    sum_select = 0
    sum_t = 0
    sum_d = 0
    for cluster in file_names:
        cluster = cluster[1:]
        rand_select = random.sample(cluster, len(cluster))

        #select files for development corpus based on PERCENT
        sum_select += len(rand_select)
        d = int(round(len(cluster) * percentage))
        dev = rand_select[:d]
        sum_d += len(dev)

        #select files for test corpus based on PERCENT
        t = int(len(cluster) - d)
        test = rand_select[-t:]
        sum_t += len(test)

        select_originals(dev, OUT1)
        sum += len(dev)
        select_originals(test, OUT2)
        sum += len(test)
    print 'sum: ', sum
    print 'sum_select: ', sum_select
    print 'sum_t: ', sum_t
    print 'sum_d: ', sum_d
    print 'sum_total: ', sum_t + sum_d
    print len(file_names)
'''
def select_originals(file_list, dir):
    for f in file_list:
        exists = False
        if __txt(f, dir):
            exists = True
        else:
            f = f[:-4]
            for m in mitredocs:
                if m(f, dir):
                    exists = True
                    break
        if not exists:
            print ('{}: was not found DEVELOPMENT'.format(f))
'''

def select_originals(file_list, dir):
    for f in file_list:
        if __txt(f, dir):
            exists = True
        else:
            exists = False
            f = f[:-4]
            for m in mitredocs:
                if m(f, dir):
                    exists = True
                    break
        if not exists:
            print ('{}: was not found DEVELOPMENT'.format(f))


DIR = '/home/andrew/Desktop/Cyber_Corpus'
OUT1 = '/home/andrew/Desktop/CyberDEV'
OUT2 = '/home/andrew/Desktop/CyberTest'

random_select(percentage=.82)