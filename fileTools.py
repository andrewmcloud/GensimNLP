__author__ = 'andrew'

import os

def verify_filesave(filename, writedir):
    counter_check = 0
    overwrite = False
    while os.path.exists(os.path.join(writedir, filename)):
        if overwrite == True:
            break
        if counter_check > 0:
            print('{} already exists.'.format(filename))
        yesno = True
        while yesno:
            save = raw_input('Overwrite existing file? [y/n]: ')
            if save == 'n':
                filename = raw_input('Input new filename: ')
                yesno = False
                counter_check += 1
            elif save == 'y':
                yesno = False
                overwrite = True
            else:
                print('Please provide a y or an n')
    print filename
    return filename