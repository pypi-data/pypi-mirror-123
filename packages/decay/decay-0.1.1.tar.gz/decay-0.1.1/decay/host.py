# -*- coding: utf-8 -*-
"""
Contains the definition of the
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('decay.host')


class DecayHost(object):
    """
    Can host one or several decay items, and contains the characteristics
    of the decay (type, duration).

    The usual use case is a list of items that inherits from this class while
    the items inherit from DecayItem. Thus the type of decay and the time
    it takes for an item's strength to decay are set in a central place
    (this class). Each item can have their own values in their journey
    from 1.0 to 0.0

    Attributes:
        decay_type (DecayType):
            an instance of the DecayType class that describes the way
            values change over time.
        decay_tics_to_0 (int):
            Number of tics (where tics can be any unit of time)
            required for a strength to go from 1.0 to 0.0
    """
    def __init__(self, decay_type=None, decay_tics_to_0=None, *args, **kwargs):
        """ Constructor. """
        super().__init__(*args, **kwargs)
        self.decay_type = decay_type
        self.decay_tics_to_0 = decay_tics_to_0

    @property
    def decay_type_id(self):
        """ Returns a numeric id of the type. """
        return self.decay_type.decay_type_id
