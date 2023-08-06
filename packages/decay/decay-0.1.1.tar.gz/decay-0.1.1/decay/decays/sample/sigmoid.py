# -*- coding: utf-8 -*-
"""
Contains the definition of the SigmoidDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.sigmoid')


class SigmoidDecay(SampleBasedDecay):
    """
    Class that decays the value following the sigmoid curve.

    Sigmoid is:
                 k
    Y = --------------------- + 1
                 a + bx
            1 + e

    This curve used a=5, b=-10, k=-1
    This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(SigmoidDecay, self).__init__(
            decay_name='.decay.sigmoid.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'SigmoidDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'SigmoidDecay()'

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
        0.9887233930500594,
        0.981060202331128,
        0.9683560429143016,
        0.9475856461385416,
        0.9143873364615575,
        0.8631975029868619,
        0.7884803317042178,
        0.6877183092063931,
        0.5654124132133331,
        0.4345875867866671,
        0.3122816907936069,
        0.21151966829578206,
        0.13680249701313818,
        0.08561266353844266,
        0.05241435386145843,
        0.03164395708569834,
        0.018939797668871994,
        0.011276606949940704,
        0.0,
    ])
