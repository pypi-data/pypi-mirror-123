# -*- coding: utf-8 -*-
"""
Contains the definition of the CubeDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.cube')


class CubeDecay(SampleBasedDecay):
    """
    Class that decays the value following the circle curve.

    The equation used to generate the samples was X^2 + Y^2 = 1.
     This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(CubeDecay, self).__init__(
            decay_name='.decay.cube.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'CubeDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'CubeDecay()'

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
        0.9998542061525003,
        0.998833649220003,
        0.9960635661175098,
        0.9906691937600234,
        0.9817757690625456,
        0.9685085289400788,
        0.949992710307625,
        0.9253535500801866,
        0.8937162851727657,
        0.8542061525003646,
        0.805948388977985,
        0.7480682315206298,
        0.679690917043301,
        0.5999416824610002,
        0.5079457646887301,
        0.40282840064149306,
        0.283714827234291,
        0.14973028138212585,
        0.0,
    ])
