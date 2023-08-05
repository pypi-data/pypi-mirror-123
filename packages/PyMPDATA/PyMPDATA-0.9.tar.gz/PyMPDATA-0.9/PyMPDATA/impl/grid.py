import numba

from PyMPDATA.impl.domain_decomposition import make_subdomain
from PyMPDATA.impl.meta import META_N_OUTER, META_N_MID3D, META_N_INNER


def make_chunk(n, n_threads, jit_flags):
    static = n > 0

    subdomain = make_subdomain(jit_flags)

    if static:
        rngs = tuple([subdomain(n, th, n_threads) for th in range(n_threads)])

        @numba.njit(**jit_flags)
        def _impl(_, thread_id):
            return rngs[thread_id]
    else:
        @numba.njit(**jit_flags)
        def _impl(meta, thread_id):
            return subdomain(meta[META_N_OUTER], thread_id, n_threads)

    return _impl


def make_domain(grid, jit_flags):
    static = grid[0] > 0

    if static:
        @numba.njit(**jit_flags)
        def _impl(_):
            return grid
    else:
        @numba.njit(**jit_flags)
        def _impl(meta):
            return meta[META_N_OUTER], meta[META_N_MID3D], meta[META_N_INNER]
    return _impl
