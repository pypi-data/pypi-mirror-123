# ElasticityPy

A small python library running a rust back-end for computation of linear elastic problems in 3D. The package relies on
quadratic tetrahedral finite elements.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install elasticitypy.

```bash
pip install elasticitypy
```

## Usage

The Mesh object requires a list of point tuples, pts = [(x0,y0,z0), (x1,y1,z1), ...] and a list tetrahedra node tuples,
tets = [(0,1,2,3), (2,5,6,10), ...], to initialize.

Define groups using boolean functions. Always use all three coordinates x,y,z for all function definitions. Groups are
used to define Dirichlet boundary conditions and may also be used to set volume forces on part of the domain. If no
group is chosen when setting a volume force, a default group is used.

```python
from elasticitypy import Mesh, Dom

mesh = Mesh(pts, tets)
left = mesh.def_group(lambda x, y, z: x == 0.)
right = mesh.def_group(lambda x, y, z: x == 2.)

dom = Dom(mesh)
dom.embed_bc(lambda x, y, z: [0., 0., 0.], left)
dom.embed_bc(lambda x, y, z: [0., 0., 0.], right)
dom.set_f(lambda x, y, z: [0., 0., x * x])

cmat = [[1., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 1., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 1., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 1., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 1., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 1., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 1., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 1., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 1.]]

dom.set_cmat(cmat)

dom.solve()
sol = dom.sol
```

## Plotting

ElasticityPy offers two functions in order to extract graphical data in the form of lines

```python
lines = dom.plot_dom()
disp = dom.plot_disp()
```

The functions return a dictionary of line-coordinates. The first function returns lines with two points, the second
returns lines with three points (parabolas).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

ElasticityPy is licensed under [GNU LGPLv3](https://choosealicense.com/licenses/lgpl-3.0).

This software relies on the [PyO3](https://github.com/PyO3/pyo3) library under
the [Apache-2.0](https://choosealicense.com/licenses/apache-2.0/) license for ffi
and on the [rayon](https://github.com/rayon-rs/rayon) crate under the [MIT](https://choosealicense.com/licenses/mit/#) 
and [Apache-2.0](https://choosealicense.com/licenses/apache-2.0/) 
licenses for parallelism.
