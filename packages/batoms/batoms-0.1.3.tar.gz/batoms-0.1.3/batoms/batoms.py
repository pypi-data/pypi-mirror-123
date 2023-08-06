"""
Definition of the Batoms class in the batoms package.

"""

import bpy
from ase import Atoms
from batoms.batom import Batom
from batoms.bondsetting import Bondsetting, build_bondlists, calc_bond_data
from batoms.polyhedrasetting import Polyhedrasetting, build_polyhedralists
from batoms.isosurfacesetting import Isosurfacesetting
from batoms.cell import Bcell
from batoms.render import Render   
from batoms.boundary import search_boundary, search_bond
from batoms.bdraw import draw_cell_cylinder, draw_bond_kind, draw_polyhedra_kind, \
                        draw_isosurface
from batoms.butils import object_mode
import numpy as np
from time import time

import logging
logging.basicConfig(
                    format=('%(levelname)-8s '
                            '[%(funcName)-20s]: %(message)s'),
                    level=logging.INFO)

logger = logging.getLogger(__name__)

subcollections = ['atom', 'cell', 'bond', 'polyhedra', 'instancer', 
'instancer_atom', 'volume', 'ghost', 'boundary', 'skin', 'render', 'text']

class Batoms():
    """
    Batoms object

    The Batoms object is a interface to a batoms collection in Blender.
    A batoms collections is organised in the following way, 
    take water molecule as a example:

    * h2o                          # main collection

      * h2o_atom                   # atoms collection
    
        * atom_h2o_H               # atoms object
    
        * atom_h2o_O               # atoms object

      * h2o_bond                   # bonds collection

        * bond_h2o_H               # bond object
    
        * bond_h2o_O               # bond object
    
      * h2o_cell                   # cell collection
    
      * h2o_instancer              # instancer collection
    
        * instancer_atom_h2o_H     # sphere object
    
        * instancer_atom_h2o_O     # sphere object
    
    Then, a Batoms object is linked to this main collection in Blender. 

    Parameters:

    label: str
        Name for the collection in Blender.
    species: dict or list
        Can be a dict with symbols and positions. Examples:
        {
         'O': [[0, 0, 0.40]], 
         'H': [[0, -0.76, -0.2], [0, 0.76, -0.2]]
        }
        Or can be a list of Baom object.
        [Batom('h2o', 'H', ...), Batom('h2o', 'O', ...)]
    atoms: ase.atoms.Atoms object or a list of ase.atoms.Atoms object
        or pymatgen structure object
    model_type: int
        enum in [0, 1, 2, 3], Default value: 0
    pbc: Bool or three Bool
        Periodic boundary conditions. Examples: True,
        False, (True, False, False).  Default value: False.
    cell: 3x3 matrix or length 3 or 6 vector
        Unit cell.
    segments: list
        value should be int, and in [3, 100000]
        segments and ring_count in bpy.ops.mesh.primitive_uv_sphere_add

    boundary:  list 
        search atoms at the boundary

    Examples:

    >>> from batoms import Batoms
    >>> h2o = Batoms(label = 'h2o', species = {'O': [[0, 0, 0.40]], 
    ...             'H': [[0, -0.76, -0.2], [0, 0.76, -0.2]]})
    
    Here is equivalent:
    
    >>> h = Batom(label = 'h2o', species = 'H', 
    ...           positions = [[0, -0.76, -0.2], [0, 0.76, -0.2]])
    >>> o = Batom(label = 'h2o', species = 'O', 
    ...           positions = [[0, 0, 0.40]])
    >>> h2o = Batoms('h2o', [h, o])

    """
    

    def __init__(self, label = None,
                species = None,
                atoms = None, 
                pbc = False, cell = None,
                bondsetting = None,
                polyhedrasetting = None,
                render = None,
                model_type = 0, 
                polyhedra_type = 0, 
                boundary = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                show_unit_cell = True,
                volume = None,
                segments = [32, 16],
                shape = 'UV_SPHERE',
                kind_props = {},
                color_style = 'JMOL',
                material_style = 'default',
                bsdf_inputs = None,
                movie = False,
                draw = True, 
                 ):
        #
        self.parent = None
        self.bondsetting = bondsetting
        self.polyhedrasetting = polyhedrasetting
        self.render = render
        self.segments = segments
        self.shape = shape
        self.kind_props = kind_props
        self.label = label
        self.color_style = color_style
        self.material_style = material_style
        self.bsdf_inputs = bsdf_inputs
        if species:
            if not self.label:
                self.label = ''.join(['%s%s'%(species, len(positions)) 
                             for sp, positions in species.items()])
            self.set_collection(model_type, polyhedra_type, boundary)
            self.from_species(species, pbc, cell)
        elif atoms:
            if isinstance(atoms, list):
                self.images = atoms
                atoms = self.images[0]
            self.set_collection(model_type, polyhedra_type, boundary)
            if 'ase' in str(type(atoms)):
                self.from_ase(atoms)
            elif 'pymatgen' in str(type(atoms)):
                self.from_pymatgen(atoms)
        elif self.label:
            print('Build from collection')
            self.from_collection(self.label)
        else:
            raise Exception("Failed, species, atoms or coll  \
                  should be provided!"%self.label)
        if not self.bondsetting:
            self.bondsetting = Bondsetting(self.label)
        if not self.polyhedrasetting:
            self.polyhedrasetting = Polyhedrasetting(self.label)
        self.isosurfacesetting = Isosurfacesetting(self.label, volume = volume)
        self.coll.batoms.show_unit_cell = show_unit_cell
        if not self.render:
            self.render = Render(self.label, batoms = self)
        if draw:
            self.draw()
        if movie:
            self.load_frames()
        self.show_index()
    def from_species(self, species, pbc = None, cell = None):
        """
        """
        if isinstance(species, dict):
            for sp, positions in species.items():
                if sp not in self.kind_props: self.kind_props[sp] = {}
                ba = Batom(self.label, sp, positions, segments = self.segments, 
                            shape = self.shape, props = self.kind_props[sp], 
                            material_style=self.material_style, 
                            bsdf_inputs=self.bsdf_inputs, color_style=self.color_style)
                self.coll.children['%s_atom'%self.label].objects.link(ba.batom)
                self.coll.children['%s_instancer'%self.label].objects.link(ba.instancer)
        elif isinstance(species, list):
            for batom in species:
                if not isinstance(batom, Batom):
                    raise Exception('%s is not a Batom object.'%batom)
                self.coll.children['%s_atom'%self.label].objects.link(batom.batom)
                self.coll.children['%s_instancer'%self.label].objects.link(batom.instancer)
        self._cell = Bcell(self.label, cell)
        self.coll.children['%s_cell'%self.label].objects.link(self._cell.bcell)
        self.set_pbc(pbc)
    def from_ase(self, atoms):
        """
        Import structure from ASE atoms.
        """
        if 'species' not in atoms.info:
            atoms.info['species'] = atoms.get_chemical_symbols()
        species_list = list(set(atoms.info['species']))
        for species in species_list:
            indices = [index for index, x in enumerate(atoms.info['species']) 
                        if x == species]
            if species not in self.kind_props: self.kind_props[species] = {}
            ba = Batom(self.label, species, atoms.positions[indices], 
                        segments = self.segments, shape = self.shape, 
                        props = self.kind_props[species], 
                        material_style=self.material_style, 
                        bsdf_inputs=self.bsdf_inputs, 
                        color_style=self.color_style)
            self.coll.children['%s_atom'%self.label].objects.link(ba.batom)
            self.coll.children['%s_instancer'%self.label].objects.link(ba.instancer)
        self.coll.batoms.pbc = self.npbool2bool(atoms.pbc)
        self._cell = Bcell(self.label, atoms.cell)
        self.coll.children['%s_cell'%self.label].objects.link(self._cell.bcell)
    def from_pymatgen(self, structure):
        """
        Import structure from Pymatgen structure.
        """
        symbols = [str(site.specie.symbol) for site in structure]
        if hasattr(structure, "lattice"):
            cell = structure.lattice.matrix
            pbc = True
        else:
            cell = None
            pbc = False
        species_list = list(set(symbols))
        for species in species_list:
            positions = [structure[index].coords for index, x 
                           in enumerate(symbols) if x == species]
            ba = Batom(self.label, species, positions, segments = self.segments, 
                       shape = self.shape, material_style=self.material_style, 
                       bsdf_inputs=self.bsdf_inputs, color_style=self.color_style)
            self.coll.children['%s_atom'%self.label].objects.link(ba.batom)
            self.coll.children['%s_instancer'%self.label].objects.link(ba.instancer)
        self.set_pbc(pbc)
        self._cell = Bcell(self.label, cell)
        self.coll.children['%s_cell'%self.label].objects.link(self._cell.bcell)
    def from_collection(self, collection_name):
        """
        """
        if collection_name not in bpy.data.collections:
            raise Exception("%s is not a collection!"%collection_name)
        elif not bpy.data.collections[collection_name].batoms.is_batoms:
            raise Exception("%s is not Batoms collection!"%collection_name)
        self.label = collection_name
        self._cell = Bcell(label = collection_name)
        self.bondsetting = Bondsetting(self.label)

    def npbool2bool(self, pbc):
        """
        """
        newpbc = []
        for i in range(3):
            if pbc[i]:
                newpbc.append(True)
            else:
                newpbc.append(False)
        return newpbc
    def set_collection(self, model_type = 0, polyhedra_type = 0, boundary = [0, 0, 0]):
        """
        build main collection and its child collections.
        """
        for coll in bpy.data.collections:
            if self.label == coll.name:
                raise Exception("Failed, the name %s already in use!"%self.label)
        coll = bpy.data.collections.new(self.label)
        self.coll.batoms.is_batoms = True
        self.scene.collection.children.link(self.coll)
        for sub_name in subcollections:
            subcoll = bpy.data.collections.new('%s_%s'%(self.label, sub_name))
            self.coll.children.link(subcoll)
        self.coll.batoms.model_type = str(model_type)
        self.coll.batoms.polyhedra_type = str(polyhedra_type)
        self.coll.batoms.boundary = boundary
    
    def draw_cell(self, celllinewidth = 0.03):
        """
        Draw unit cell
        """
        object_mode()
        cell_vertices = self.cell.verts
        if np.max(abs(cell_vertices)) < 1e-6:
            return 0
        self.clean_atoms_objects('cell', ['cylinder', 'point'])
        if self.show_unit_cell:
            draw_cell_cylinder(self.coll.children['%s_cell'%self.label], 
                            cell_vertices, 
                            label = self.label, 
                            celllinewidth = celllinewidth)
    def draw_bonds(self):
        """
        Draw bonds.

        Parameters:

        cutoff: float
            cutoff used to build bond pairs.
        """
        # if not self.bondlist:
        object_mode()
        self.clean_atoms_objects('bond')
        atoms = self.get_atoms_with_boundary()
        self.bondlist = build_bondlists(atoms, self.bondsetting.cutoff_dict)
        bond_kinds = calc_bond_data(self, self.bondlist, self.bondsetting)
        for species, bond_data in bond_kinds.items():
            draw_bond_kind(species, bond_data, label = self.label, 
                        coll = self.coll.children['%s_bond'%self.label])
    def draw_polyhedras(self, bondlist = None, show_edge = True):
        """
        Draw bonds.
        Parameters:

        cutoff: float
            cutoff used to build bond pairs.
        """
        object_mode()
        self.clean_atoms_objects('polyhedra')
        atoms = self.get_atoms_with_boundary(X = True)
        if bondlist is None:
            bondlist = build_bondlists(atoms, self.bondsetting.cutoff_dict)
        polyhedra_kinds = build_polyhedralists(atoms, bondlist, 
                          self.bondsetting, self.polyhedrasetting)
        for species, polyhedra_data in polyhedra_kinds.items():
            draw_polyhedra_kind(species, polyhedra_data, label = self.label,
                        coll = self.coll.children['%s_polyhedra'%self.label], show_edge = show_edge)
    def draw_isosurface(self):
        """
        Draw bonds.

        Parameters:

        isosurface: list
            isosurface data.
        """
        object_mode()
        self.clean_atoms_objects('volume', ['isosurface'])
        isosurface = self.isosurfacesetting.build_isosurface(self.cell)
        for verts, faces, color in isosurface:
            draw_isosurface(self.coll.children['%s_volume'%self.label],
                            verts, faces, color = color)
    def draw_cavity_sphere(self, radius, boundary = [[0, 1], [0, 1], [0, 1]]):
        """
        cavity
        for porous materials
        >>> from ase.io import read
        >>> atoms = read('docs/source/_static/datas/mof-5.cif')
        """
        from batoms.tools import find_cage_sphere
        object_mode()
        self.clean_atoms_objects('ghost')
        positions = find_cage_sphere(self.cell, self.atoms.positions, radius, boundary = boundary)
        ba = Batom(self.label, 'X', positions, scale = radius*0.9, 
                   material_style='default', bsdf_inputs=self.bsdf_inputs, 
                   color_style=self.color_style)
        
        # ba.color = [ba.color[0], ba.color[1], ba.color[2], 0.8]
        self.coll.children['%s_ghost'%self.label].objects.link(ba.batom)
        self.coll.children['%s_ghost'%self.label].objects.link(ba.instancer)
    def draw_cavity(self, bondlists = None):
        """
        cavity
        for porous materials
        >>> from ase.io import read
        >>> atoms = read('docs/source/_static/datas/mof-5.cif')
        """
        from batoms.tools import find_cage
        from batoms.bdraw import draw_cavity
        object_mode()
        self.clean_atoms_objects('ghost')
        atoms = self.get_atoms_with_boundary()
        positions = atoms.positions
        if bondlists is None:
            bondlists = build_bondlists(atoms, self.bondsetting.cutoff_dict)
        # calc data
        vertices = []
        edges = []
        # offset = bondlists[:, 2:5]
        # R = np.dot(offset, atoms.cell)
        # pos1 = positions[bondlists[:, 0]]
        # pos2 = positions[bondlists[:, 1]] + R
        # n = len(pos1)
        # vertices = np.append(pos1, pos2, axis = 0)
        # index1 = np.array(range(n)).reshape(-1, 1)
        # index2 = np.array(range(n)).reshape(-1, 1) + n
        # edges = np.append(index1, index2, axis = 1)
        edges = bondlists[:, [0, 1]]
        edges.astype(int)
        edges = edges.tolist()
        # draw edge based on bonds
        kind = 'cavity'
        datas = {'vertices': positions, 'edges': edges, 'color': [0.4, 0.4, 0.1], 'transmit': 1.0}
        draw_cavity(kind, datas, self.label, coll = self.coll.children['%s_polyhedra'%self.label])
        
    def clean_atoms_objects(self, coll, names = None):
        """
        remove all bond object in the bond collection
        """
        if not names:
            for obj in self.coll.children['%s_%s'%(self.label, coll)].all_objects:
                bpy.data.objects.remove(obj, do_unlink = True)
        else:
            for name in names:
                for obj in self.coll.children['%s_%s'%(self.label, coll)].all_objects:
                    if name in obj.name:
                        bpy.data.objects.remove(obj, do_unlink = True)
                
    def show_index(self, index_type = 0):
        """
        """
        bpy.context.preferences.view.show_developer_ui = True
        for a in bpy.context.screen.areas:
            if a.type == 'VIEW_3D':
                overlay = a.spaces.active.overlay
                overlay.show_extra_indices = True
    @property
    def scene(self):
        return self.get_scene()
    def get_scene(self):
        return bpy.data.scenes['Scene']
    @property
    def scale(self):
        return self.get_scale()
    @scale.setter
    def scale(self, scale):
        self.set_scale(scale)
    def get_scale(self):
        scale = {}
        for coll in [self.batoms, self.batoms_boundary, self.batoms_skin]:
            for batom in coll.values():
                scale[batom.species] = batom.scale
        return scale
    def set_scale(self, scale):
        for coll in [self.batoms, self.batoms_boundary, self.batoms_skin]:
            for batom in coll.values():
                batom.scale = scale
    def draw(self, model_type = None):
        """
        Draw atoms, bonds, polyhedra.

        Parameters:

        model_type: str

        """
        if model_type is not None and model_type not in [0, 1, 2, 3]:
            raise Exception('model_type %s should be: 0, 1, 2, 3'%model_type)
        if not model_type:
            model_type = self.model_type
        else:
            self.model_type = model_type
        # self.draw_cell()
        bpy.ops.ed.undo_push()
        self.clean_atoms_objects('bond')
        bpy.ops.ed.undo_push()
        self.clean_atoms_objects('polyhedra')
        bpy.ops.ed.undo_push()
        if model_type == 0:
            self.scale = 1.0
        elif model_type == 1:
            self.scale = 0.4
            self.draw_bonds()
        elif model_type == 2:
            if self.polyhedra_type == 0:
                self.scale = 0.4
                self.draw_bonds()
                self.draw_polyhedras(self.bondlist)
            if self.polyhedra_type == 1:
                self.scale = 0.4
                self.draw_polyhedras()
            elif self.polyhedra_type == 2:
                self.scale = 0.01
                for b in self.bondsetting:
                    if b.polyhedra:
                        self.batoms[b.symbol1].scale = 0.4
                self.draw_polyhedras()
            elif self.polyhedra_type == 3:
                self.scale = 0.01
                self.draw_polyhedras()
        elif model_type == 3:
            self.scale = 0.01
            self.draw_bonds()
        if self.isosurfacesetting.npoint > 0:
            self.draw_isosurface()
    def replace(self, species1, species2, index = []):
        """
        replace atoms.

        Parameters:
        
        index: list
            index of atoms will be replaced.

        species1: str

        species2: str
            atoms will be changed to this element.

        >>> from ase.build import molecule, fcc111
        >>> from batoms.batoms import Batoms
        >>> pt111 = fcc111('Pt', (5, 5, 4), vacuum = 5.0)
        >>> pt111 = Batoms(atoms = pt111, label = 'pt111')
        >>> pt111.replace('Pt', 'Au', [93])
        >>> pt111.replace('Pt', 'Au', range(20))

        """
        # if kind exists, merger, otherwise build a new kind and add.
        object_mode()
        positions = self.batoms[species1].positions[index]
        if species2 in self.batoms:
            self.batoms[species2].add_vertices(positions)
        else:
            ba = Batom(self.label, species2, positions, segments = self.segments, 
                       shape = self.shape, material_style=self.material_style, 
                       bsdf_inputs=self.bsdf_inputs, color_style=self.color_style)
            self.coll.children['%s_atom'%self.label].objects.link(ba.batom)
            self.coll.children['%s_instancer'%self.label].objects.link(ba.instancer)
            for sp in self.species:
                self.bondsetting.add_bonds([[species2, sp]])
            self.polyhedrasetting.add_polyhedras([sp])
        self.batoms[species1].delete(index)
            
    
    def delete(self, species, index = []):
        """
        delete atoms.

        species: str

        index: list
            index of atoms to be delete
        
        For example, delete the second atom in H species.
        Please note that index start from 0.

        >>> h2o.delete([1])

        """
        self.batoms[species].delete(index)
    def translate(self, displacement):
        """Translate atomic positions.

        The displacement argument is an xyz vector.

        For example, move h2o molecule by a vector [0, 0, 5]

        >>> h2o.translate([0, 0, 5])

        """
        object_mode()
        bpy.ops.object.select_all(action='DESELECT')
        for obj in self.coll.all_objects:
            if 'instancer' not in obj.name and 'boundary' not in obj.name:
                obj.select_set(True)
        bpy.ops.transform.translate(value=displacement)
    def rotate(self, angle, axis = 'Z', orient_type = 'GLOBAL'):
        """Rotate atomic based on a axis and an angle.

        Parameters:

        angle: float
            Angle that the atoms is rotated around the axis.
        axis: str
            'X', 'Y' or 'Z'.

        For example, rotate h2o molecule 90 degree around 'Z' axis:
        
        >>> h2o.rotate(90, 'Z')

        """
        object_mode()
        bpy.ops.object.select_all(action='DESELECT')
        for coll in self.coll.children:
            for obj in coll.objects:
                obj.select_set(True)
        bpy.ops.transform.rotate(value=angle, orient_axis=axis.upper(), 
                                 orient_type = orient_type)
    
    def __getitem__(self, species):
        """Return a subset of the Batom.

        species -- str, describing which batom to return.
        """

        if isinstance(species, str):
            if species not in self.batoms:
                raise SystemExit('%s is not in this structure'%species)
            return self.batoms[species]
        elif isinstance(species, list):
            raise SystemExit('dict not supported yet!')
    def __len__(self):
        return len(self.positions)
    def __repr__(self) -> str:
        text = []
        text.append('label={0}, '.format(self.label))
        text.append('species='.format(self.cell))
        text.append('%s '%(list(self.batoms)))
        text.append('cell={0}, '.format(self.cell))
        text.append('pbc={0}'.format(self.pbc))
        text = "".join(text)
        text = "Batoms(%s)"%text
        return text
    def __add__(self, other):
        self += other
        return self
    def __iadd__(self, other):
        self.extend(other)
        return self
    def extend(self, other):
        """
        Extend batoms object by appending batoms from *other*.
        
        >>> from ase.build import molecule, fcc111
        >>> from batoms.batoms import Batoms
        >>> import numpy as np
        >>> co = molecule('CO')
        >>> co = Batoms(atoms = co, draw = True)
        >>> au = fcc111('Au', (5, 5, 4), vacuum=5.0)
        >>> au = Batoms(atoms = au, draw = True)
        >>> co.translate(au.atoms[-1].position + np.array([0, 0, 2]))
        >>> au.extend(co)
        >>> au.write('au111-co.cif')
        
        or,

        >>> au = au + co

        """
        from batoms.butils import remove_collection
        # bond first
        self.bondsetting.extend(other.bondsetting)
        self.polyhedrasetting.extend(other.polyhedrasetting)
        # atom
        for species, batom in other.batoms.items():
            if species in self.species:
                self.batoms[species].extend(batom)
            else:
                ba = batom.copy(self.label, species)
                t = self.cell.location - ba.location
                ba.batom.location = self.cell.location
                bpy.context.view_layer.update()
                ba.positions = ba.positions - t
                self.coll.children['%s_atom'%self.label].objects.link(ba.batom)
        remove_collection(other.label)
    def __imul__(self, m):
        """
        """
        for species, batom in self.batoms.items():
            batom.repeat(m, self.cell)
        self.cell.repeat(m)
        self.draw()
    def repeat(self, rep):
        """
        Create new repeated atoms object.

        >>> from ase.build import bulk
        >>> from batoms.batoms import Batoms
        >>> au = bulk('Au', cubic = True)
        >>> au = Batoms(atoms = au)
        >>> au.draw()
        >>> au.repeat([2, 2, 2])
        
        """
        self.__imul__(rep)
    def __mul__(self, rep):
        self.repeat(rep)
        return self
    def copy(self, label = None):
        """
        Return a copy.

        name: str
            The name of the copy.

        For example, copy h2o molecule:
        
        >>> h2o_new = h2o.copy(label = 'h2o_new')

        """
        if not label:
            label = self.label + 'copy'
        species_dict = {x:self.batoms[x].copy(label, x) for x in self.species}
        batoms = self.__class__(species = species_dict, label = label, 
                                cell = self.cell.verts, pbc = self.pbc, 
                                model_type = self.coll.batoms.model_type)
        batoms.translate([2, 2, 2])
        batoms.bondsetting = self.bondsetting.copy(label)
        batoms.polyhedrasetting = self.polyhedrasetting.copy(label)
        return batoms
    def write(self, filename, local = True):
        """
        Save atoms to file.

        >>> h2o.write('h2o.cif')
        
        """
        atoms = self.batoms2atoms(self.batoms, local = local)
        atoms.write(filename)
    def update(self):
        """
        """
        pass
    @property
    def coll(self):
        return self.get_coll()
    def get_coll(self):
        return bpy.data.collections[self.label]
    @property
    def coll_atom(self):
        return self.get_coll_atom()
    def get_coll_atom(self):
        return self.coll.children['%s_atom'%self.label]
    @property
    def coll_boundary(self):
        return self.get_coll_boundary()
    def get_coll_boundary(self):
        return self.coll.children['%s_boundary'%self.label]
    @property
    def coll_skin(self):
        return self.get_coll_skin()
    def get_coll_skin(self):
        return self.coll.children['%s_skin'%self.label]
    @property
    def cell(self):
        return self._cell
    @cell.setter
    def cell(self, cell):
        from ase.cell import Cell
        cell = Cell.ascell(cell)
        self._cell[:] = cell
    def set_cell(self, cell, scale_atoms=False):
        """Set unit cell vectors.

        Parameters:

        Examples:

        """
        from ase.cell import Cell
        from ase.geometry.cell import complete_cell

        cell = Cell.new(cell)
        oldcell = Cell(self.cell)
        self.cell = cell
        if scale_atoms:
            M = np.linalg.solve(oldcell.complete(), cell.complete())
            for ba in self.batoms.values():
                ba.positions = np.dot(ba.positions(), M)
    @property
    def pbc(self):
        return self.get_pbc()
    @pbc.setter
    def pbc(self, pbc):
        self.set_pbc(pbc)
    def get_pbc(self):
        return list(self.coll.batoms.pbc)
    def set_pbc(self, pbc):
        if isinstance(pbc, bool):
            pbc = [pbc]*3
        self.coll.batoms.pbc = pbc
    @property
    def boundary(self):
        return self.get_boundary()
    @boundary.setter
    def boundary(self, boundary):
        if boundary is not None:
            if isinstance(boundary, (int, float)):
                boundary = np.array([-boundary, 1 + boundary]*3)
            elif len(boundary) == 3:
                if isinstance(boundary[0], (int, float)):
                    boundary = np.array([[-boundary[0], 1 + boundary[0]],
                                      [-boundary[1], 1 + boundary[1]],
                                      [-boundary[2], 1 + boundary[2]]])
                elif len(boundary[0]) == 2:
                    boundary = np.array(boundary)
            else:
                raise Exception('Wrong boundary setting!')
            self.coll.batoms.boundary = boundary[:].flatten()
        self.update_boundary()
    def get_boundary(self):
        boundary = np.array(self.coll.batoms.boundary)
        return boundary.reshape(3, -1)
    def update_boundary(self):
        """
        >>> from batoms.batoms import Batoms
        >>> from ase.io import read
        >>> atoms = read('docs/source/_static/datas/tio2.cif')
        >>> tio2 = Batoms(label = 'tio2', atoms = atoms, model_type = '2', 
            polyhedra_dict = {'Ti': ['O']}, color_style="VESTA")
        >>> tio2.boundary = 0.4
        """
        tstart = time()
        boundary = self.boundary
        atoms0 = self.atoms
        if atoms0.pbc.any():
            # find boudary atoms
            atoms_boundary, offsets_skin = search_boundary(atoms0, boundary, self.bondsetting.maxcutoff)
            self.draw_boundary_atoms(atoms_boundary)
            # search bond
            # include the boundary atoms
            bondlists = build_bondlists(atoms0, self.bondsetting.cutoff_dict)
            offsets_skin1, bondlist1, offsets_skin2, bondlist2 = \
                    self.bondsetting.search_bond_list(atoms0, bondlists, offsets_skin)
            # search type 1
            offset_skin_1 = search_bond(atoms0.get_scaled_positions(), offsets_skin1, bondlist1, boundary)
            # search type 2
            offset_skin_2 = search_bond(atoms0.get_scaled_positions(), offsets_skin2, bondlist2, boundary, recursive=True)
            # search type 1 final
            offset_skin_3 = search_bond(atoms0.get_scaled_positions(), offset_skin_2, bondlist1, boundary)
            self.draw_search_bond_atoms(atoms0, offset_skin_1, offset_skin_2, offset_skin_3)
            # print('search skin: {0:10.2f} s'.format(time() - tstart))
    def draw_boundary_atoms(self, atoms_boundary):
        self.clean_atoms_objects('boundary')
        if len(atoms_boundary) == 0: return 0
        species = set(atoms_boundary.info['species'])
        for sp in species:
            positions = atoms_boundary[atoms_boundary.info['species']==sp].positions
            positions = positions + self.batoms[sp].location
            ba = Batom(self.label, '%s_boundary'%(sp), positions, scale = self.batoms[sp].scale, 
                        segments = self.segments, shape = self.shape, material=self.batoms[sp].material)
            self.coll.children['%s_boundary'%self.label].objects.link(ba.batom)
    def draw_search_bond_atoms(self, atoms0, offsets_search_1, offsets_search_2, offsets_search_3):
        # print(atoms)
        self.clean_atoms_objects('skin')
        offsets_search = np.append(offsets_search_1, offsets_search_2, axis = 0)
        offsets_search = np.append(offsets_search, offsets_search_3, axis = 0)
        if len(offsets_search) == 0: return 0
        offsets_search = offsets_search.astype(int)
        atoms_search_bond = atoms0[offsets_search[:, 0]]
        atoms_search_bond.positions = atoms_search_bond.positions + np.dot(offsets_search[:, 1:], atoms0.cell)
        atoms_search_bond.info['species'] = np.array(atoms0.info['species'])[offsets_search[:, 0]]
        species = set(atoms_search_bond.info['species'])
        for sp in species:
            positions = atoms_search_bond[atoms_search_bond.info['species']==sp].positions
            positions = positions + self.batoms[sp].location
            ba = Batom(self.label, '%s_skin'%(sp), positions, scale = self.batoms[sp].scale, 
                        segments = self.segments, shape = self.shape, material=self.batoms[sp].material)
            self.coll.children['%s_skin'%self.label].objects.link(ba.batom)
        # print('update skin: {0:10.2f} s'.format(time() - tstart))

    @property
    def model_type(self):
        return self.get_model_type()
    @model_type.setter
    def model_type(self, model_type):
        self.set_model_type(model_type)
    def get_model_type(self):
        return int(self.coll.batoms.model_type)
    def set_model_type(self, model_type):
        self.coll.batoms.model_type = str(model_type)
        self.draw()
    @property
    def polyhedra_type(self):
        return self.get_polyhedra_type()
    @polyhedra_type.setter
    def polyhedra_type(self, polyhedra_type):
        self.set_polyhedra_type(polyhedra_type)
    def get_polyhedra_type(self):
        return int(self.coll.batoms.polyhedra_type)
    def set_polyhedra_type(self, polyhedra_type):
        self.coll.batoms.polyhedra_type = str(polyhedra_type)
        self.draw()
    @property
    def show_unit_cell(self):
        return self.get_show_unit_cell()
    @show_unit_cell.setter
    def show_unit_cell(self, show_unit_cell):
        self.set_show_unit_cell(show_unit_cell)
    def get_show_unit_cell(self):
        return self.coll.batoms.show_unit_cell
    def set_show_unit_cell(self, show_unit_cell):
        self.coll.batoms.show_unit_cell = show_unit_cell
        self.draw_cell()
    def get_atoms(self, batoms):
        return self.batoms2atoms(batoms)
    @property
    def atoms(self):
        return self.get_atoms(self.batoms)
    @property
    def atoms_boundary(self):
        return self.get_atoms(self.batoms_boundary)
    @property
    def atoms_skin(self):
        return self.get_atoms(self.batoms_skin)
    def get_atoms_with_boundary(self, X = False):
        """
        build ASE atoms from batoms dict.
        """
        atoms = self.batoms2atoms(self.batoms, X = X)
        atoms_boundary = self.batoms2atoms(self.batoms_boundary, X = X)
        atoms_skin = self.batoms2atoms(self.batoms_skin, X = X)
        species = atoms.info['species'] + atoms_boundary.info['species'] + atoms_skin.info['species']
        atoms = atoms + atoms_boundary + atoms_skin
        atoms.info['species'] = species
        atoms.pbc = False
        return atoms
    @property
    def positions(self):
        return self.get_positions()
    def get_positions(self):
        return self.atoms.positions
    def get_scaled_positions(self):
        return self.atoms.get_scaled_positions()
    @property
    def species(self):
        return self.get_species()
    def get_species(self):
        """
        build species from collection.
        """
        species = []
        for ba in self.coll_atom.objects:
            species.append(ba.batom.species)
        return species
    @property
    def batoms(self):
        return self.get_batoms()
    def get_batoms(self):
        batoms = {}
        for ba in self.coll_atom.objects:
            batoms[ba.batom.species] = Batom(ba.name)
        return batoms
    @property
    def batoms_boundary(self):
        return self.get_batoms_boundary()
    def get_batoms_boundary(self):
        batoms_boundary = {}
        for ba in self.coll_boundary.objects:
            batoms_boundary[ba.batom.species] = Batom(ba.name)
        return batoms_boundary
    @property
    def batoms_skin(self):
        return self.get_batoms_skin()
    def get_batoms_skin(self):
        batoms_skin = {}
        for ba in self.coll_skin.objects:
            batoms_skin[ba.batom.species] = Batom(ba.name)
        return batoms_skin
    def batoms2atoms(self, batoms, local = False, X = False):
        object_mode()
        atoms = Atoms()
        species_list = []
        symbols = []
        positions = []
        for species, batom in batoms.items():
            # ghost site will not save 
            if not X and batom.element == 'X': continue
            if species[-9:] == '_boundary': species = species[0:-9]
            if species[-5:] == '_skin': species = species[0:-5]
            species_list.extend([species]*len(batom))
            symbol = [batom.element]*len(batom)
            symbols.extend(symbol)
            if local:
                positions.extend(batom.local_positions)
            else:
                positions.extend(batom.positions)
        atoms = Atoms(symbols, positions, cell = self.cell, pbc = self.pbc)
        atoms.info['species'] = species_list
        return atoms
    def draw_constraints(self):
        """
        """
        #
        constr = self.atoms.constraints
        self.constrainatoms = []
        for c in constr:
            if isinstance(c, FixAtoms):
                for n, i in enumerate(c.index):
                    self.constrainatoms += [i]
    
    def highlight_atoms(self, indexs, shape = 'sphere', radius_scale=1.4,
                           color=(0.0, 1.0, 0.0), transmit=0.6):
        """
        """
        object_mode()
        for index in indexs:
            loc = self.positions[index]
            ele = self.symbols[index]
            radii = radius_scale * self.atom_kinds[ele]['radius']
            if shape == 'cube':
                bpy.ops.mesh.primitive_cube_add(location=loc, size=radii*2)
            else:
                bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=radii)
            ball = bpy.context.view_layer.objects.active
            bpy.ops.object.shade_smooth()
            ball.data.materials.append(material)
            ball.show_transparent = True
            self.coll_highlight.objects.link(ball)
    def load_frames(self, images = None):
        """

        images: list
            list of atoms. All atoms show have same species and length.
            
        >>> from ase.io import read
        >>> from batoms import Batoms
        >>> images = read('h2o-animation.xyz', index = ':')
        >>> h2o = Batoms(label = 'h2o', atoms = images)
        >>> h2o.load_frames()
        >>> h2o.render(animation = True)

        """
        if not images:
            images = self.images
        if len(self.atoms) != len(images[0]):
            raise Exception("Number of atoms %s is not equal to %s."%(len(self.atoms), len(images[0])))
        atoms = images[0]
        if 'species' not in atoms.info:
            atoms.info['species'] = atoms.get_chemical_symbols()
        positions = np.array([atoms.positions for atoms in images])
        for species, ba in self.batoms.items():
            index = [atom.index for atom in atoms if atoms.info['species'][atom.index] == species]
            ba.load_frames(positions[:, index])
    
    def calc_camera_data(self, canvas, canvas1, direction = (0, 0, 1)):
        """
        """
        from scipy.spatial.transform import Rotation as R
        camera_target = np.mean(canvas, axis=0)
        camera_data = {}
        width = canvas1[1, 0] - canvas1[0, 0]
        height = canvas1[1, 1] - canvas1[0, 1]
        depth = canvas1[1, 1] - canvas1[0, 1]
        ortho_scale = max(width, height)
        #
        direction = direction/np.linalg.norm(direction)
        location = camera_target + direction*depth
        camera_data = {'camera_loc': location, 'camera_target': camera_target,
                        'ortho_scale': ortho_scale, 'ratio': height/width}
        return camera_data  

    def get_distances(self, species1, i, species2, indices, mic=False):
        """
        Return distances of atom No.i with a list of atoms.

        Use mic=True to use the Minimum Image Convention.

        >>> h2o.get_distances('O', 0, 'H', [0, 1])
        """
        from ase.geometry import get_distances

        p1 = self.batoms[species1][i]
        p2 = self.batoms[species2][indices]
        cell = None
        pbc = None
        if mic:
            cell = self.cell
            pbc = self.pbc
        D, D_len = get_distances(p1, p2, cell=cell, pbc=pbc)
        D_len.shape = (-1,)
        return D_len
    def get_angle(self, species1, i1, species2, i2, species3, i3, mic=False):
        """
        Get angle in degrees between the vectors i2->i1 and
        i2->i3.
        Use mic=True to use the Minimum Image Convention and calculate the
        angle across periodic boundaries.

        >>> h2o.get_angle('H', 0, 'O', 0, 'H', 1)

        """
        from ase.geometry import get_angles
        p1 = self.batoms[species1][i1]
        p2 = self.batoms[species2][i2]
        p3 = self.batoms[species3][i3]
        v12 = p1 - p2
        v32 = p3 - p2
        cell = None
        pbc = None
        if mic:
            cell = self.cell
            pbc = self.pbc
        return get_angles([v12], [v32], cell=cell, pbc=pbc)
    def get_center_of_mass(self, scaled=False):
        """Get the center of mass.

        If scaled=True the center of mass in scaled coordinates
        is returned."""
        return self.atoms.get_center_of_mass(scaled = scaled)
