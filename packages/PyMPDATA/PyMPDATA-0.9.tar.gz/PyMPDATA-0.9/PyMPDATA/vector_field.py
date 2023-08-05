import inspect
import numpy as np
from PyMPDATA.impl.enumerations import (
    MAX_DIM_NUM, OUTER, MID3D, INNER, INVALID_NULL_VALUE, INVALID_INIT_VALUE, INVALID_HALO_VALUE
)
from PyMPDATA.scalar_field import ScalarField
from PyMPDATA.impl.meta import META_HALO_VALID, META_IS_NULL
from PyMPDATA.boundary_conditions.constant import Constant
from PyMPDATA.impl.field import Field


class VectorField(Field):
    def __init__(self, data, halo, boundary_conditions):
        assert len(data) == len(boundary_conditions)

        super().__init__(grid=tuple([data[d].shape[d] - 1 for d, _ in enumerate(data)]))

        for comp, field in enumerate(data):
            assert len(field.shape) == len(data)
            for dim, dim_length in enumerate(field.shape):
                assert halo <= dim_length
                if not (np.asarray(self.grid) == 0).all():
                    assert dim_length == self.grid[dim] + (dim==comp)
        for bc in boundary_conditions:
            assert not inspect.isclass(bc)

        self.halo = halo
        self.n_dims = len(data)
        self.dtype = data[0].dtype

        dims = range(self.n_dims)
        halos = [[(halo - (d == c)) for c in dims] for d in dims]
        shape_with_halo = [
            [data[d].shape[c] + 2 * halos[d][c] for c in dims]
            for d in dims
        ]
        self.data = [
            np.full(shape_with_halo[d], INVALID_INIT_VALUE, dtype=self.dtype)
            for d in dims
        ]
        self.domain = tuple([
            tuple([
                slice(halos[d][c], halos[d][c] + data[d].shape[c])
                for c in dims])
            for d in dims
        ])
        for d in dims:
            assert data[d].dtype == self.dtype
            self.get_component(d)[:] = data[d][:]
        self.boundary_conditions = boundary_conditions

        self.fill_halos = [None] * MAX_DIM_NUM
        self.fill_halos[OUTER] = boundary_conditions[OUTER] \
            if self.n_dims > 1 else Constant(INVALID_HALO_VALUE)
        self.fill_halos[MID3D] = boundary_conditions[MID3D] \
            if self.n_dims > 2 else Constant(INVALID_HALO_VALUE)
        self.fill_halos[INNER] = boundary_conditions[INNER]
        self.comp_outer = self.data[0] \
            if self.n_dims > 1 else np.empty(tuple([0] * self.n_dims), dtype=self.dtype)
        self.comp_mid3d = self.data[1] \
            if self.n_dims > 2 else np.empty(tuple([0] * self.n_dims), dtype=self.dtype)
        self.comp_inner = self.data[-1]
        self.impl = None
        self.jit_flags = None

    def assemble(self, traversals):
        if traversals.jit_flags != self.jit_flags:
            self.impl = (self.meta, self.comp_outer, self.comp_mid3d, self.comp_inner), tuple([
                fh.make_vector(
                    traversals.indexers[self.n_dims].at[i],
                    self.dtype,
                    traversals.jit_flags
                )
                for i, fh in enumerate(self.fill_halos)
            ])
        self.jit_flags = traversals.jit_flags

    @staticmethod
    def clone(field):
        return VectorField([
            field.get_component(d)
            for d in range(field.n_dims)
        ], field.halo, field.boundary_conditions)

    def get_component(self, i: int) -> np.ndarray:
        return self.data[i][self.domain[i]]

    def div(self, grid_step: tuple) -> ScalarField:
        diff_sum = None
        for d in range(self.n_dims):
            tmp = np.diff(self.get_component(d), axis=d) / grid_step[d]
            if diff_sum is None:
                diff_sum = tmp
            else:
                diff_sum += tmp
        result = ScalarField(diff_sum,
                             halo=0,
                             boundary_conditions=[Constant(INVALID_HALO_VALUE)] * len(grid_step)
                             )
        return result

    @staticmethod
    def make_null(n_dims, indexers):
        null = VectorField(
            [np.full([1] * n_dims, INVALID_NULL_VALUE)] * n_dims,
            halo=1,
            boundary_conditions=[Constant(INVALID_HALO_VALUE)] * n_dims
        )
        null.meta[META_HALO_VALID] = True
        null.meta[META_IS_NULL] = True
        null.assemble(indexers)
        return null
