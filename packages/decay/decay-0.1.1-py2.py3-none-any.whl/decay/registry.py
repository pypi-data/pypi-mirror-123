# -*- coding: utf-8 -*-
"""
The type of decays provided by the library are available in a concise form
in the registry. The users of the library may add other types by
using the dedicated methods.
"""
from .decays import (
    NoDecay, LinearDecay, CircleDecay, CubeDecay, HalfSuddenDecay,
    InverseCircleDecay, InverseParabolaDecay,
    ParabolaDecay, SigmoidDecay, SquareRootDecay, SuddenDecay,
    ThreeSinesDecay
)
from .constants import (
    NO_DECAY, LINEAR_DECAY, CIRCLE_DECAY, CUBE_DECAY, HALF_SUDDEN_DECAY,
    INVERSE_CIRCLE_DECAY, INVERSE_PARABOLA_DECAY, PARABOLA_DECAY,
    SIGMOID_DECAY, SQUARE_ROOT_DECAY, SUDDEN_DECAY, THREE_SINES_DECAY,
)


class Registry(object):
    """
    Stores all types of decays known to the library.
    """
    def __init__(self):
        global registry
        super().__init__()

        assert registry is None
        registry = self

        self.id_to_type = {}
        self.name_to_type = {}
        self.name_to_id = {}

        self._lib_init()

    @staticmethod
    def instance():
        return registry

    def add_type(self, kind, numeric_id):
        self.id_to_type[numeric_id] = kind
        self.name_to_type[kind.decay_name] = kind
        self.name_to_id[kind.decay_name] = numeric_id

    def remove_type(self, kind, numeric_id):
        del self.id_to_type[numeric_id]
        del self.name_to_type[kind.decay_name]

    def _lib_init(self):
        self.add_type(NoDecay(), NO_DECAY)
        self.add_type(LinearDecay(), LINEAR_DECAY)
        self.add_type(CircleDecay(), CIRCLE_DECAY)
        self.add_type(CubeDecay(), CUBE_DECAY)
        self.add_type(HalfSuddenDecay(), HALF_SUDDEN_DECAY)
        self.add_type(InverseCircleDecay(), INVERSE_CIRCLE_DECAY)
        self.add_type(InverseParabolaDecay(), INVERSE_PARABOLA_DECAY)
        self.add_type(ParabolaDecay(), PARABOLA_DECAY)
        self.add_type(SigmoidDecay(), SIGMOID_DECAY)
        self.add_type(SquareRootDecay(), SQUARE_ROOT_DECAY)
        self.add_type(SuddenDecay(), SUDDEN_DECAY)
        self.add_type(ThreeSinesDecay(), THREE_SINES_DECAY)


registry = Registry()
