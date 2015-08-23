__author__ = 'andrew'
import os
import shutil as sh


def verify_filesave(writedir, filename):

    if not writedir=='':
        if not os.path.exists(writedir):
            os.makedirs(writedir)

    counter_check = 0
    overwrite = False
    while os.path.exists(os.path.join(writedir, filename)):
        if overwrite == True:
            break
        if counter_check > 0:
            print('{} already exists.'.format(filename))
        yesno = True
        while yesno:
            save = raw_input('Overwrite existing file: {}? [y/n]: '.format(filename))
            if save == 'n':
                filename = raw_input('Input new filename: ')
                yesno = False
                counter_check += 1
            elif save == 'y':
                yesno = False
                overwrite = True
            else:
                print('Please provide a y or an n')
    # print filename
    return filename


def comma_exclude(csv_exclude_file, folder_path):
    count = 0
    #Ensure DEV_DIR exists
    if not os.path.exists(os.path.join(folder_path, 'excluded')):
        os.makedirs(os.path.join(folder_path, 'excluded'))

    if not os.path.exists(csv_exclude_file):
        print ('{} path does not exist'.format(csv_exclude_file))
    f = open(csv_exclude_file, 'r')
    x = f.read()

    #Load comma separated file names into list: file_names[]
    file_names = []
    for exclude in x.split(','):
        exclude = exclude.strip()
        file_path = os.path.join(folder_path, exclude)
        exclude_path = os.path.join(folder_path, 'excluded', exclude)
        print 'filepath: {}'.format(file_path)
        print 'excludepath: {}'.format(exclude_path)
        sh.move(file_path, exclude_path)

'''
#MAIN
import validatePDF
def main():
    #comma_exclude(*validatePDF.validate_pdf(readdir='/home/andrew/Desktop/test_corpus,
    #                                        writedir='/home/andrew/Desktop', per_dict_words=.80, unicode=False))

    comma_exclude('/home/andrew/Desktop/Cyber_Corpus/TXTexclude70.csv', '/home/andrew/Desktop/Cyber_Corpus/TXT')

    #validatePDF.validate_pdf(readdir='/home/andrew/Desktop/Cyber_Corpus/TXT',
    #                         writedir='/home/andrew/Desktop/Cyber_Corpus', per_dict_words=.70, unicode=True)
if __name__ == '__main__':
    main()
'''
