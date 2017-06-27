import os
from contextlib import contextmanager

from gaus_parse import open_file, parse_coords, parse_constants
from sqlalchemy import Column, Integer, String, Float, Boolean, Enum,\
                       ForeignKey, DateTime, PickleType,\
                       LargeBinary, create_engine

from sqlalchemy.orm import backref, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

@contextmanager
def open_temporary_session(db_name, echo=False):
    ''' convenience function to get
    session for non standard database '''
    engine = create_engine('sqlite:///%s' % db_name, echo=echo)
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

class BaseDB:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=BaseDB)

class Molecule(Base):
    __tablename__ = 'molecule'
    atoms = relationship('Atom', backref='molecule')
    name = Column(String)
    file = Column(String)
    mass = Column(Integer)
    chemspyder_id = Column(Integer)
    constants = relationship('Constants', backref='molecule')
    constants_id = Column(Integer, ForeignKey('constants.id'))

    @classmethod
    def from_file(cls, filepath):

        instance = cls()

        instance.chemspyder_id, *instance.name = os.path.basename(filepath).replace('.out', '').split('_')
        if isinstance(instance.name, list):
            instance.name = '_'.join(instance.name)

        data = open_file(filepath)
        instance.constants = Constants.from_string(**parse_constants(data))
        instance.atoms = [Atom(gauss_data=line) for line in parse_coords(data)]
        return instance

    def __repr__(self):
        return 'Molecule({})'.format(self.name)

    def __str__(self):
        return self.__repr__()

class Constants(Base):
    A = Column(Float)
    B = Column(Float)
    C = Column(Float)
    uA = Column(Float)
    uB = Column(Float)
    uC = Column(Float)
    uTotal = Column(Float)

    @classmethod
    def from_string(cls, abc, quad, dipole):
        instance = cls()

        instance.A, instance.B, instance.C = [float(rot) for rot in abc.split()]
        ua, ub, uc, _, total = dipole.split()

        instance.uA = float(ua)
        instance.uB = float(ub)
        instance.uC = float(uc)
        instance.total = float(total)
        return instance

    def __repr__(self):
        return 'Constants({},{},{})'.format(self.A, self.B, self.C)

class Coords(Base):
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)

    def __init__(self, *, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Atom(Base):
    coords = relationship('Coords', backref=backref('atom', uselist=False))
    coords_id = Column(Integer, ForeignKey('coords.id'))
    _number = Column(Integer)
    atomic_num = Column(Integer)
    molecule_id = Column(Integer, ForeignKey('molecule.id'))

    def __init__(self, *, gauss_data=None):
        split_data = gauss_data.split()

        if gauss_data is not None:
            self.coords = Coords(x=split_data[2],
                                 y=split_data[3],
                                 z=split_data[4])
            self.atomic_num = int(split_data[1])
            self._number = int(split_data[0])

    def __repr__(self):
        return 'Atom({id}, {atomic_num})'.format(id=self._number,
                                                 atomic_num=self.atomic_num)

    @property
    def x(self):
        return self.coords.x

    @x.setter
    def x(self, val):
        self.coords.x = val

    @property
    def y(self):
        return self.coords.y

    @y.setter
    def y(self, val):
        self.coords.y = val

    @property
    def z(self):
        return self.coords.z

    @z.setter
    def z(self, val):
        self.coords.z = val

