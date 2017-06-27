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
    data = 'abd fdfs fsafs sasdf sddfdf .. sdf sdf'

    x = re.compile(r'fsafs(.*)sdf')

    #x = re.compile(r'(?<=Principal axis orientation:).*?(?=Rotational constants (MHZ):)')
    result = x.search(data)

    print('RESULT', result.group(1))

