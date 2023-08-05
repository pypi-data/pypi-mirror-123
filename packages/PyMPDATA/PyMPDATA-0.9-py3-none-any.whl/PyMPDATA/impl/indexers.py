from collections import namedtuple
import numba
from .enumerations import INNER, OUTER, MID3D, INVALID_INDEX

def make_indexers(jit_flags):
    @numba.njit([numba.boolean(numba.float64),
                 numba.boolean(numba.int64)], **jit_flags)
    def _is_integral(n):
        return int(n * 2.) % 2 == 0


    @numba.njit(**jit_flags)
    def at_1d(focus, arr, k, _=INVALID_INDEX, __=INVALID_INDEX):
        return arr[focus[INNER] + k]


    @numba.njit(**jit_flags)
    def at_2d_axis0(focus, arr, i, k=0, _=INVALID_INDEX):
        return arr[focus[OUTER] + i, focus[INNER] + k]


    @numba.njit(**jit_flags)
    def at_2d_axis1(focus, arr, k, i=0, _=INVALID_INDEX):
        return arr[focus[OUTER] + i, focus[INNER] + k]


    @numba.njit(**jit_flags)
    def at_3d_axis0(focus, arr, i, j=0, k=0):
        return arr[focus[OUTER] + i, focus[MID3D] + j, focus[INNER] + k]


    @numba.njit(**jit_flags)
    def at_3d_axis1(focus, arr, j, k=0, i=0):
        return arr[focus[OUTER] + i, focus[MID3D] + j, focus[INNER] + k]


    @numba.njit(**jit_flags)
    def at_3d_axis2(focus, arr, k, i=0, j=0):
        return arr[focus[OUTER] + i, focus[MID3D] + j, focus[INNER] + k]


    @numba.njit(**jit_flags)
    def atv_1d(focus, arrs, k, _=INVALID_INDEX, __=INVALID_INDEX):
        return arrs[INNER][focus[INNER] + int(k - .5)]


    @numba.njit(**jit_flags)
    def atv_2d_axis0(focus, arrs, i, k=0, _=INVALID_INDEX):
        if _is_integral(i):
            d, ii, kk = INNER, int(i), int(k - .5)
        else:
            d, ii, kk = OUTER, int(i - .5), int(k)
        return arrs[d][focus[OUTER] + ii, focus[INNER] + kk]


    @numba.njit(**jit_flags)
    def atv_2d_axis1(focus, arrs, k, i=0, _=INVALID_INDEX):
        if _is_integral(i):
            d, ii, kk = INNER, int(i), int(k - .5)
        else:
            d, ii, kk = OUTER, int(i - .5), int(k)
        return arrs[d][focus[OUTER] + ii, focus[INNER] + kk]


    @numba.njit(**jit_flags)
    def atv_3d_axis0(focus, arrs, i, j=0, k=0):
        if not _is_integral(i):
            d, ii, jj, kk = OUTER, int(i - .5), int(j), int(k)
        elif not _is_integral(j):
            d, ii, jj, kk = MID3D, int(i), int(j - .5), int(k)
        else:
            d, ii, jj, kk = INNER, int(i), int(j), int(k - .5)
        return arrs[d][focus[OUTER] + ii, focus[MID3D] + jj, focus[INNER] + kk]


    @numba.njit(**jit_flags)
    def atv_3d_axis1(focus, arrs, j, k=0, i=0):
        if not _is_integral(i):
            d, ii, jj, kk = OUTER, int(i - .5), int(j), int(k)
        elif not _is_integral(j):
            d, ii, jj, kk = MID3D, int(i), int(j - .5), int(k)
        else:
            d, ii, jj, kk = INNER, int(i), int(j), int(k - .5)
        return arrs[d][focus[OUTER] + ii, focus[MID3D] + jj, focus[INNER] + kk]


    @numba.njit(**jit_flags)
    def atv_3d_axis2(focus, arrs, k, i=0, j=0):
        if not _is_integral(i):
            d, ii, jj, kk = OUTER, int(i - .5), int(j), int(k)
        elif not _is_integral(j):
            d, ii, jj, kk = MID3D, int(i), int(j - .5), int(k)
        else:
            d, ii, jj, kk = INNER, int(i), int(j), int(k - .5)
        return arrs[d][focus[OUTER] + ii, focus[MID3D] + jj, focus[INNER] + kk]


    @numba.njit(**jit_flags)
    def set_1d(arr, _, __, k, value):
        arr[k] = value


    @numba.njit(**jit_flags)
    def set_2d(arr, i, _, k, value):
        arr[i, k] = value


    @numba.njit(**jit_flags)
    def set_3d(arr, i, j, k, value):
        arr[i, j, k] = value


    @numba.njit(**jit_flags)
    def get_1d(arr, _, __, k):
        return arr[k]


    @numba.njit(**jit_flags)
    def get_2d(arr, i, _, k):
        return arr[i, k]


    @numba.njit(**jit_flags)
    def get_3d(arr, i, j, k):
        return arr[i, j, k]


    Indexers = namedtuple('Indexers', ('at', 'atv', 'set', 'get'))

    indexers = (
        None,
        Indexers(
            (None, None, at_1d),
            (None, None, atv_1d),
            set_1d,
            get_1d
        ),
        Indexers(
            (at_2d_axis0, None, at_2d_axis1),
            (atv_2d_axis0, None, atv_2d_axis1),
            set_2d,
            get_2d
        ),
        Indexers(
            (at_3d_axis0, at_3d_axis1, at_3d_axis2),
            (atv_3d_axis0, atv_3d_axis1, atv_3d_axis2),
            set_3d,
            get_3d
        )
    )
    return indexers
