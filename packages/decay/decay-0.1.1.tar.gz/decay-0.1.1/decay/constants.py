# -*- coding: utf-8 -*-
"""
"""
import logging

__author__ = "Nicu Tofan"
__package_name__ = "decay"
__copyright__ = "Copyright 2019, Nicu Tofan"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Nicu Tofan"
__email__ = "nicu.tofan@gmail.com"
__package_url__ = 'https://github.com/pyl1b/%s' % __package_name__

# Strength below this value gets converted to 0.
STRENGTH_SMALL_ENOUGH_TO_BE_0 = 0.00001


NO_DECAY = 1
LINEAR_DECAY = 2
CIRCLE_DECAY = 3
CUBE_DECAY = 4
HALF_SUDDEN_DECAY = 5
INVERSE_CIRCLE_DECAY = 6
INVERSE_PARABOLA_DECAY = 7
PARABOLA_DECAY = 8
SIGMOID_DECAY = 9
SQUARE_ROOT_DECAY = 10
SUDDEN_DECAY = 11
THREE_SINES_DECAY = 12
