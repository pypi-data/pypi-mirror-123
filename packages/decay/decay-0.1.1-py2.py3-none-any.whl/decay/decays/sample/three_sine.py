# -*- coding: utf-8 -*-
"""
Contains the definition of the ThreeSinesDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from . import SampleBasedDecay

logger = logging.getLogger('decay.three_sines')


class ThreeSinesDecay(SampleBasedDecay):
    """
    Class that decays the value following the sine curve.

    The function will move the strength up and down three times.
    """
    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super(ThreeSinesDecay, self).__init__(
            decay_name='.decay.three_sines.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ThreeSinesDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ThreeSinesDecay()'

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
        0.3262540763928261,
        0.3278919323251512,
        0.503260272238791,
        0.6753376062071077,
        0.670424473673676,
        0.49348032194639296,
        0.3231173075182364,
        0.33130441097781665,
        0.5097773512507269,
        0.6783807718213233,
        0.6669218731749817,
        0.4869675739031233,
        0.32016855389184307,
        0.3348962024993367,
        0.5162840375492987,
        0.681234329822624,
        0.6632418451565344,
        0.4804686785143609,
        0.0,
    ])
