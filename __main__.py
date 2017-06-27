import os

from gaus_parse import file_list
from molecule import Molecule, open_temporary_session





FOLDER = os.path.join(os.path.expanduser('~'),
                      'Dropbox (BrightSpec)',
                      'BrightSpec_Data',
                      'G09_mmwlibrary',
                      'Outputs-Passed')
FOLDER = os.path.join(r'D:\Dropbox (BrightSpec)\BrightSpec_Data\G09_mmwlibrary\Outputs-Passed')


def create_db():
    with open_temporary_session('cool_db') as session:
        for i, file in enumerate(file_list(FOLDER)):

            try:
                x = Molecule.from_file(os.path.join(FOLDER, file))
                session.add(x)
            except Exception as e:
                print(e)
                print(file)

        session.commit()
if __name__ == '__main__':
    if not os.path.isfile('cool_db'):
        create_db()

    with open_temporary_session('cool_db') as session:
        x = session.query(Molecule)
        print(x.all()[0].atoms)

