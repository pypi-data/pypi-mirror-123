# -*- coding: utf-8 -*-
"""
Contains the definition of the InverseParabolaDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.inverse-parabola')


class InverseParabolaDecay(SampleBasedDecay):
    """
    Class that decays the value following the circle curve.

    The equation used to generate the samples was Y = X^2 - 2X + 1
    This intersects the Y axis at
    +1 and the X axis at -1 and +1. We're interested only in the
    positive x.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(InverseParabolaDecay, self).__init__(
            decay_name='.decay.inv_parabola.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'InverseParabolaDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'InverseParabolaDecay()'

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
        0.8975069252077562,
        0.8005540166204986,
        0.7091412742382271,
        0.6232686980609419,
        0.5429362880886427,
        0.4681440443213296,
        0.39889196675900274,
        0.33518005540166207,
        0.2770083102493075,
        0.22437673130193914,
        0.17728531855955676,
        0.1357340720221607,
        0.09972299168975074,
        0.06925207756232687,
        0.04432132963988922,
        0.024930747922437657,
        0.011080332409972304,
        0.0027700831024930483,
        0.0,
    ])

