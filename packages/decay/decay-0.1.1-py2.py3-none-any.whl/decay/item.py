# -*- coding: utf-8 -*-
"""
Contains the definition of the DecayItem class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from decay.constants import STRENGTH_SMALL_ENOUGH_TO_BE_0

logger = logging.getLogger('decay.item')


class DecayItem(object):
    """
    Contains attributes particular to a decaying item.

    Attributes:
        decay_strength (float):
            the strength of the item (subject to decay) at time decay_time
        decay_time (int):
            the last time a strength has been computed.
    """
    def __init__(self, decay_strength=1.0, decay_time=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            decay_strength (float):
                the strength of the item (subject to decay) at time decay_time
            decay_time (int):
                the last time a strength has been computed.
        """
        super().__init__(*args, **kwargs)

        self.decay_strength = decay_strength
        self.decay_time = decay_time

    def __str__(self):
        """ Represent this object as a human-readable string. """
        if self.decay_time is None:
            return 'DecayItem(#Invalid)'
        else:
            return 'DecayItem(%.1f, %d)' % (
                self.decay_strength, self.decay_time)

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'DecayItem(%r, %r)' % (
                self.decay_strength, self.decay_time)

    def set_decay(self, new_tic, new_strength):
        """ Changes the value of the strength. """
        if new_strength < STRENGTH_SMALL_ENOUGH_TO_BE_0:
            new_strength = 0.0
        elif new_strength > 1.0:
            new_strength = 1.0
        self.decay_time = new_tic
        self.decay_strength = new_strength
        return self.decay_strength
