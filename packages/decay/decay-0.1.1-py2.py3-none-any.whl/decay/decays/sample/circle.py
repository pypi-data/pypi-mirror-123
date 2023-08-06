# -*- coding: utf-8 -*-
"""
Contains the definition of the CircleDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.circle')


class CircleDecay(SampleBasedDecay):
    """
    Class that decays the value following the circle curve.

    The equation used to generate the samples was X^2 + Y^2 = 1.
     This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(CircleDecay, self).__init__(
            decay_name='.decay.circle.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'CircleDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'CircleDecay()'

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
        0.9986139979479093,
        0.9944444014574307,
        0.9874559494365115,
        0.9775881905793005,
        0.96475277788544,
        0.9488292830168393,
        0.929659038560826,
        0.9070362073481099,
        0.8806947647727111,
        0.850289180073869,
        0.8153649149910351,
        0.7753115717187492,
        0.7292845505553168,
        0.6760648725613226,
        0.6137844099837158,
        0.5393131982084001,
        0.44659375653887234,
        0.3201453963314855,
        0.0,
    ])
