# -*- coding: utf-8 -*-
"""
Contains the definition of the SquareRootDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.sqrt')


class SquareRootDecay(SampleBasedDecay):
    """
    Class that decays the value following the radical curve.

    The equation used to generate the samples was y = 1 - math.sqrt(x)
    This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(SquareRootDecay, self).__init__(
            decay_name='.decay.sqrt.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'SquareRootDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'SquareRootDecay()'

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
        0.7705842661294382,
        0.6755571577384749,
        0.6026402928804868,
        0.5411685322588764,
        0.487010823957423,
        0.4380485130509837,
        0.39302302133311606,
        0.3511143154769498,
        0.3117527983883147,
        0.2745237498899884,
        0.23911408974731785,
        0.20528058576097374,
        0.17282980813148896,
        0.1416049247210479,
        0.1114766833613614,
        0.08233706451775291,
        0.05409469707308279,
        0.026671473215424846,
        0.0,
    ])
