import numpy as np
from pystrict import strict


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


@strict
class Options:
    def __init__(self, *,
                 n_iters: int = 2,
                 infinite_gauge: bool = False,
                 divergent_flow: bool = False,
                 nonoscillatory: bool = False,
                 third_order_terms: bool = False,
                 DPDC: bool = False,
                 epsilon: float = 1e-15,
                 non_zero_mu_coeff: bool = False,
                 dimensionally_split: bool = False,
                 dtype: np.floating = np.float64
                 ):
        self._values = hashabledict({
            'n_iters': n_iters,
            'infinite_gauge': infinite_gauge,
            'epsilon': epsilon,
            'divergent_flow': divergent_flow,
            'nonoscillatory': nonoscillatory,
            'third_order_terms': third_order_terms,
            'non_zero_mu_coeff': non_zero_mu_coeff,
            'dimensionally_split': dimensionally_split,
            'dtype': dtype,
            'DPDC': DPDC
        })

        if (
            infinite_gauge or
            divergent_flow or
            nonoscillatory or
            third_order_terms or
            DPDC
        ) and n_iters < 2:
            raise ValueError()
        if n_iters < 1:
            raise ValueError()

    @property
    def dtype(self):
        return self._values['dtype']

    @property
    def n_iters(self):
        return self._values['n_iters']

    @property
    def infinite_gauge(self):
        return self._values['infinite_gauge']

    @property
    def epsilon(self):
        return self._values['epsilon']

    @property
    def divergent_flow(self):
        return self._values['divergent_flow']

    @property
    def nonoscillatory(self):
        return self._values['nonoscillatory']

    @property
    def third_order_terms(self):
        return self._values['third_order_terms']

    @property
    def DPDC(self):
        return self._values['DPDC']
    
    @property
    def non_zero_mu_coeff(self):
        return self._values['non_zero_mu_coeff']

    @property
    def dimensionally_split(self):
        return self._values['dimensionally_split']

    def __str__(self):
        return str(self._values)
    
    def __hash__(self):
        value = hash(self._values) + hash(self.jit_flags)
        return value

    def __eq__(self, other):
        return other.__hash__() == self.__hash__()

    @property
    def n_halo(self):
        if self.divergent_flow or self.nonoscillatory or self.third_order_terms:
            return 2
        else:
            return 1

    @property
    def jit_flags(self):
        return hashabledict({
            "fastmath": True,
            "error_model": 'numpy',
            "boundscheck": False,
        })
