import numba
from .meta import META_HALO_VALID
from .enumerations import (
    OUTER, MID3D, INNER, SIGN_LEFT, SIGN_RIGHT, RNG_START, RNG_STOP, INVALID_INDEX
)


def _make_apply_scalar(*, indexers, loop, jit_flags, n_dims, halo, n_threads, chunker, spanner,
                       boundary_cond_vector, boundary_cond_scalar):
    set = indexers[n_dims].set
    get = indexers[n_dims].get

    if loop:
        @numba.njit(**jit_flags)
        def apply_scalar_impl(thread_id, out_meta,
                              fun_outer, fun_mid3d, fun_inner,
                              out,
                              vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner,
                              scal_arg2, scal_arg3, scal_arg4, scal_arg5
                              ):
            span = spanner(out_meta)
            rng_outer = chunker(out_meta, thread_id)
            rng_mid3d = (0, span[MID3D])
            rng_inner = (0, span[INNER])

            vec_arg1_tpl = (vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner)
            for i in range(rng_outer[RNG_START] + halo,
                           rng_outer[RNG_STOP] + halo) if n_dims > 1 else (INVALID_INDEX,):
                for j in range(rng_mid3d[RNG_START] + halo,
                               rng_mid3d[RNG_STOP] + halo) if n_dims > 2 else (INVALID_INDEX,):
                    for k in range(rng_inner[RNG_START] + halo,
                                   rng_inner[RNG_STOP] + halo):
                        focus = (i, j, k)
                        if n_dims > 1:
                            set(out, i, j, k, fun_outer(
                                get(out, i, j, k),
                                (focus, vec_arg1_tpl),
                                (focus, scal_arg2),
                                (focus, scal_arg3),
                                (focus, scal_arg4),
                                (focus, scal_arg5)
                            ))
                            if n_dims > 2:
                                set(out, i, j, k, fun_mid3d(
                                    get(out, i, j, k),
                                    (focus, vec_arg1_tpl),
                                    (focus, scal_arg2),
                                    (focus, scal_arg3),
                                    (focus, scal_arg4),
                                    (focus, scal_arg5)
                                ))
                        set(out, i, j, k, fun_inner(
                            get(out, i, j, k),
                            (focus, vec_arg1_tpl),
                            (focus, scal_arg2),
                            (focus, scal_arg3),
                            (focus, scal_arg4),
                            (focus, scal_arg5)
                        ))
    else:
        @numba.njit(**jit_flags)
        def apply_scalar_impl(thread_id, out_meta,
                              fun, _, __,
                              out,
                              vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner,
                              scal_arg2, scal_arg3, scal_arg4, scal_arg5
                              ):
            span = spanner(out_meta)
            rng_outer = chunker(out_meta, thread_id)
            rng_mid3d = (0, span[MID3D])
            rng_inner = (0, span[INNER])

            vec_arg1_tpl = (vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner)
            for i in range(rng_outer[RNG_START] + halo,
                           rng_outer[RNG_STOP] + halo) if n_dims > 1 else (INVALID_INDEX,):
                for j in range(rng_mid3d[RNG_START] + halo,
                               rng_mid3d[RNG_STOP] + halo) if n_dims > 2 else (INVALID_INDEX,):
                    for k in range(rng_inner[RNG_START] + halo,
                                   rng_inner[RNG_STOP] + halo):
                        focus = (i, j, k)
                        set(out, i, j, k, fun(
                            get(out, i, j, k),
                            (focus, vec_arg1_tpl),
                            (focus, scal_arg2),
                            (focus, scal_arg3),
                            (focus, scal_arg4),
                            (focus, scal_arg5)
                        ))

    @numba.njit(**{**jit_flags, **{'parallel': n_threads > 1}})
    def apply_scalar(fun_outer, fun_mid3d, fun_inner,
                     out_meta, out,
                     vec_arg1_meta, vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner,
                     vec_arg1_bc_outer, vec_arg1_bc_mid3d, vec_arg1_bc_inner,
                     scal_arg2_meta, scal_arg_2, scal_arg2_bc_outer, scal_arg2_bc_mid3d, scal_arg2_bc_inner,
                     scal_arg3_meta, scal_arg_3, scal_arg3_bc_outer, scal_arg3_bc_mid3d, scal_arg3_bc_inner,
                     scal_arg4_meta, scal_arg_4, scal_arg4_bc_outer, scal_arg4_bc_mid3d, scal_arg4_bc_inner,
                     scal_arg5_meta, scal_arg_5, scal_arg5_bc_outer, scal_arg5_bc_mid3d, scal_arg5_bc_inner,
                     ):
        for thread_id in range(1) if n_threads == 1 else numba.prange(n_threads):
            boundary_cond_vector(thread_id, vec_arg1_meta, vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner, vec_arg1_bc_outer, vec_arg1_bc_mid3d, vec_arg1_bc_inner)
            boundary_cond_scalar(thread_id, scal_arg2_meta, scal_arg_2, scal_arg2_bc_outer, scal_arg2_bc_mid3d, scal_arg2_bc_inner)
            boundary_cond_scalar(thread_id, scal_arg3_meta, scal_arg_3, scal_arg3_bc_outer, scal_arg3_bc_mid3d, scal_arg3_bc_inner)
            boundary_cond_scalar(thread_id, scal_arg4_meta, scal_arg_4, scal_arg4_bc_outer, scal_arg4_bc_mid3d, scal_arg4_bc_inner)
            boundary_cond_scalar(thread_id, scal_arg5_meta, scal_arg_5, scal_arg5_bc_outer, scal_arg5_bc_mid3d, scal_arg5_bc_inner)
        if not vec_arg1_meta[META_HALO_VALID]:
            vec_arg1_meta[META_HALO_VALID] = True
        if not scal_arg2_meta[META_HALO_VALID]:
            scal_arg2_meta[META_HALO_VALID] = True
        if not scal_arg3_meta[META_HALO_VALID]:
            scal_arg3_meta[META_HALO_VALID] = True
        if not scal_arg4_meta[META_HALO_VALID]:
            scal_arg4_meta[META_HALO_VALID] = True
        if not scal_arg5_meta[META_HALO_VALID]:
            scal_arg5_meta[META_HALO_VALID] = True

        for thread_id in range(1) if n_threads == 1 else numba.prange(n_threads):
            apply_scalar_impl(
                thread_id, out_meta,
                fun_outer, fun_mid3d, fun_inner,
                out,
                vec_arg1_outer, vec_arg1_mid3d, vec_arg1_inner,
                scal_arg_2, scal_arg_3, scal_arg_4, scal_arg_5
            )
        out_meta[META_HALO_VALID] = False

    return apply_scalar


def _make_fill_halos_scalar(*, indexers, jit_flags, halo, n_dims, chunker, spanner):
    set = indexers[n_dims].set

    @numba.njit(**jit_flags)
    def boundary_cond_scalar(thread_id, meta, psi, fun_outer, fun_mid3d, fun_inner):
        if meta[META_HALO_VALID]:
            return

        span = spanner(meta)
        rng_outer = chunker(meta, thread_id)
        last_thread = rng_outer[RNG_STOP] == span[OUTER]

        if n_dims > 2:
            for i in range(rng_outer[RNG_START],
                           rng_outer[RNG_STOP] + (2 * halo if last_thread else 0)):
                for k in range(0, span[INNER] + 2 * halo):
                    for j in range(halo - 1, -1, -1):  # note: reversed order for Extrapolated!
                        focus = (i, j, k)
                        set(psi, i, j, k, fun_mid3d((focus, psi), span[MID3D], SIGN_LEFT))
                    for j in range(span[MID3D] + halo, span[MID3D] + 2 * halo):
                        focus = (i, j, k)
                        set(psi, i, j, k, fun_mid3d((focus, psi), span[MID3D], SIGN_RIGHT))

        if n_dims > 1:
            if thread_id == 0:
                for i in range(halo - 1, -1, -1):  # note: reversed order assumed in Extrapolated
                    for j in range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,):
                        for k in range(0, span[INNER] + 2 * halo):
                            focus = (i, j, k)
                            set(psi, i, j, k, fun_outer((focus, psi), span[OUTER], SIGN_LEFT))
            if last_thread:
                for i in range(span[OUTER] + halo,
                               span[OUTER] + 2*halo):  # note: non-reversed order for Extrapolated
                    for j in range(0,
                                   span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,):
                        for k in range(0,
                                       span[INNER] + 2 * halo):
                            focus = (i, j, k)
                            set(psi, i, j, k, fun_outer((focus, psi), span[OUTER], SIGN_RIGHT))

        for i in range(rng_outer[RNG_START],
                       rng_outer[RNG_STOP] + (2 * halo if last_thread else 0)
                       ) if n_dims > 1 else (INVALID_INDEX,):
            for j in range(0,
                           span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,):
                for k in range(halo - 1,
                               -1, -1):  # note: reversed order assumed in Extrapolated!
                    focus = (i, j, k)
                    set(psi, i, j, k, fun_inner((focus, psi), span[INNER], SIGN_LEFT))
                for k in range(span[INNER] + halo,
                               span[INNER] + 2 * halo):
                    focus = (i, j, k)
                    set(psi, i, j, k, fun_inner((focus, psi), span[INNER], SIGN_RIGHT))

    return boundary_cond_scalar
