# -*- coding: utf-8 -*-
"""
Contains the definition of the SuddenDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.half_sudden')


class HalfSuddenDecay(SampleBasedDecay):
    """
    Class that decays the value following the sigmoid curve.

    Sigmoid is:
                 k
    Y = --------------------- + 1
                 a + bx
            1 + e

    This curve used a=10, b=-10, k=-2
    This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(HalfSuddenDecay, self).__init__(
            decay_name='.decay.half_sudden.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'SuddenDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'SuddenDecay()'

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
        0.9998463162863197,
        0.9997398757902081,
        0.9995597314205974,
        0.999254877774581,
        0.9987390684889199,
        0.9978665723466811,
        0.9963914462121438,
        0.9938994809709213,
        0.9896955173948945,
        0.9826197888368629,
        0.9707568136416107,
        0.9509968204584932,
        0.9184373437414545,
        0.8657330022308358,
        0.7828273568190789,
        0.6581107760257361,
        0.4825598285864794,
        0.2572468384313463,
        0.0,
    ])
