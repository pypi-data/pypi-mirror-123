# -*- coding: utf-8 -*-
"""
Contains the definition of the InverseCircleDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.inverse-circle')


class InverseCircleDecay(SampleBasedDecay):
    """
    Class that decays the value following the circle curve.

    The equation used to generate the samples was (X - 1)^2 + (Y - 1)^2 = R^1.
    This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(InverseCircleDecay, self).__init__(
            decay_name='.decay.inv_circle.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'InverseCircleDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'InverseCircleDecay()'

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
        0.6798546036685147,
        0.5534062434611279,
        0.46068680179160004,
        0.38621559001628425,
        0.3239351274386775,
        0.2707154494446832,
        0.2246884282812508,
        0.18463508500896486,
        0.149710819926131,
        0.11930523522728897,
        0.09296379265189014,
        0.07034096143917401,
        0.05117071698316078,
        0.035247222114559995,
        0.022411809420699536,
        0.012544050563488507,
        0.005555598542569262,
        0.001386002052090718,
        0.0,
    ])

