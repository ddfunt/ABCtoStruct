import os
import re

def file_list(folder):
    return os.listdir(folder)



def open_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()

    return data

def parse_coords(data):
    x = re.compile(r'Principal axis orientation: (.*?)Rotational constants', re.DOTALL)

    result = x.search(data)
    lines = result.group(1).splitlines()[5:-2]
    for line in lines:
        yield line

def parse_constants(data):
    'Nuclear quadrupole coupling constants'

    x = re.compile(r'Principal axis orientation: (.*?)Nuclear quadrupole coupling constants', re.DOTALL)
    result = x.search(data)
    abc = result.group(1).splitlines()[-2]

    dp_search = re.compile(r'Principal axis orientation: (.*?)Atoms with significant hyperfine tensors', re.DOTALL)
    result = dp_search.search(data)
    dipole = result.group(1).splitlines()[-3]
    return {
        'abc': abc,
        'quad': None,
        'dipole': dipole
    }




