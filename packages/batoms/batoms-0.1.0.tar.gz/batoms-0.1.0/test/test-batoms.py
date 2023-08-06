import pytest
from batoms.batom import Batom
from batoms.batoms import Batoms
from batoms.butils import removeAll
import numpy as np


def test_batom():
    removeAll()
    h = Batom(label = 'h2o', species = 'H', positions = [[0, -0.76, -0.2], [0, 0.76, -0.2]])
    o = Batom(label = 'h2o', species = 'O', positions = [[0, 0, 0.40]])
    h2o = Batoms('h2o', [h, o])
    assert isinstance(h2o, Batoms)

def test_batoms():
    """
    """
    removeAll()
    h2o = Batoms('h2o', {'O': [[0, 0, 0.40]], 'H': [[0, -0.76, -0.2], [0, 0.76, -0.2]]})
    assert isinstance(h2o, Batoms)
    # properties
    h2o.cell = [3, 3, 3]
    h2o.pbc = True
    h2o.model_type = 1
    h2o.translate([0, 0, 2])
    #
    h2o_2 = h2o.copy('h2o_2')
    assert isinstance(h2o_2, Batoms)
    h2o_3 = Batoms(label='h2o_2')
    #
    # delete
    del h2o_3['H'][[0]]
    assert len(h2o_3['H']) == 1
    #
    h2o_3.replace('O', 'C', [0])
    #
    h2o['O'][0] = [0, 0, 2.0]
    index = [0, 1]
    h2o['H'][index][:, 0] += 2

def test_extend():
    from ase.build import molecule
    co = molecule('CO')
    co = Batoms(label = 'co', atoms = co)
    co.translate([0, 0, 2])
    h2o = molecule('H2O')
    h2o = Batoms(label = 'h2o', atoms = h2o)
    h2o.extend(co)


def test_canvas():
    from ase.build import fcc111
    from batoms.batoms import Batoms
    from batoms.butils import removeAll
    removeAll()
    atoms = fcc111('Pt', size = (4, 4, 4), vacuum=0)
    pt111 = Batoms(label = 'pt111', atoms = atoms)
    pt111.cell[2, 2] += 5
    pt111.render([1, 1, 1])

def test_batoms_animation():
    from ase.build import molecule
    removeAll()
    atoms = molecule('C2H6SO')
    images = []
    for i in range(20):
        temp = atoms.copy()
        temp.rotate(18*i, 'z')
        images.append(temp)
    c2h6so = Batoms(label = 'c2h6so', atoms = images)
    c2h6so.load_frames()
    # c2h6so.render(animation = True)

def test_cavity():
    from batoms.bio import read
    from batoms.butils import removeAll
    removeAll()
    mof = read('../../docs/source/_static/datas/mof-5.cif')
    mof.draw_cavity_sphere(9.0, boundary = [[0.2, 0.8], [0.2, 0.8], [0.2, 0.8]])
    mof.model_type = 2
    mof.draw_cell()
    mof.render.light_energy = 30
    mof.render.run([1, 0, 0], engine = 'eevee')

def test_get_angles():
    from ase.build import molecule
    atoms = molecule('H2O')
    h2o = Batoms(atoms = atoms, label = 'h2o')
    angle = h2o.get_angle('H', 0, 'O', 0, 'H', 1)
    d = h2o.get_distances('H', 0, 'H', 1)



if __name__ == '__main__':
    test_batoms()
    test_batoms_animation()
    test_cavity()
    test_get_angles()
    print('\n Batoms: All pass! \n')