class Molecule:
    atoms = []
    name = ''
    file = ''
    mass = -1




class Atom:
    coords = [0, 0, 0]

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, val):
        self.coords[0] = val

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, val):
        self.coords[1] = val

    @property
    def z(self):
        return self.coords[2]

    @z.setter
    def z(self, val):
        self.coords[2] = val