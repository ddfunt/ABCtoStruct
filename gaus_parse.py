import os
import re

FOLDER = os.path.join(os.path.expanduser('~'),
                      'Dropbox (BrightSpec)',
                      'BrightSpec_Data',
                      'G09_mmwlibrary',
                      'Outputs-Passed')


def file_list(folder):
    return os.listdir(folder)



def open_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()

    return data





if __name__ == '__main__':

    file = file_list(FOLDER)[0]
    data = open_file(os.path.join(FOLDER, file))
    #print(data)
    #data = 'abd fdfs fsafs\n sasdf sddfdf .. sdf sdf'

    #x = re.compile(r'fsafs(.*)sdf', re.DOTALL)
    if 'rincipal axis orientation:' in data:
        print(True)
    if 'Rotational constants' in data:
        print(True)
    x = re.compile(r'Principal axis orientation(.*?)Rotational constants', re.DOTALL)

    result = x.search(data)

    print('RESULT', result.group())

