# -*- coding: utf-8 -*-
"""
Contains the definition of the ParabolaDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.parabola')


class ParabolaDecay(SampleBasedDecay):
    """
    Class that decays the value following the parabola curve.

    The equation used to generate the samples was Y = mX + b, with
    m being -1 and b being 1. This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(ParabolaDecay, self).__init__(
            decay_name='.decay.parabola.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ParabolaDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ParabolaDecay()'

    decay_x = np.array([
        0.0,
        0.05263157894736842,
        0.10526315789473684,
        0.15789473684210525,
        0.21052631578947367,
        0.2631578947368421,
        0.3157894736842105,
        0.3684210526315789,
        0.42105263157894735,
        0.47368421052631576,
        0.5263157894736842,
        0.5789473684210527,
        0.631578947368421,
        0.6842105263157894,
        0.7368421052631579,
        0.7894736842105263,
        0.8421052631578947,
        0.894736842105263,
        0.9473684210526315,
        1.0,
    ])

    decay_y = np.array([
        1.0,
        0.997229916897507,
        0.9889196675900277,
        0.9750692520775623,
        0.9556786703601108,
        0.9307479224376731,
        0.9002770083102494,
        0.8642659279778393,
        0.8227146814404432,
        0.775623268698061,
        0.7229916897506925,
        0.6648199445983379,
        0.6011080332409973,
        0.5318559556786705,
        0.4570637119113574,
        0.3767313019390581,
        0.29085872576177296,
        0.1994459833795016,
        0.1024930747922439,
        0.0,
    ])
