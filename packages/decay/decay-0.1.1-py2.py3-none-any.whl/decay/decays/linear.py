# -*- coding: utf-8 -*-
"""
Contains the definition of the NoDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from decay.kind import DecayType

logger = logging.getLogger('decay.linear')


class LinearDecay(DecayType):
    """
    This is a decay placeholder that does not change the strength.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(decay_name='.decay.linear.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'LinearDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'LinearDecay()'

    def update_decay(self, item, host, tic):
        """
        Change the value of the strength based on the time passed since th
        last update.

        Args:
            item:
                the item whose strength we're updating.
            host:
                the way we should update the item.
            tic:
                time at which we should compute the strength.

        Returns:
            Computed strength
        """
        logger.log(1, "linear decay for item %s hosted in %s at time %r",
                   item, host, tic)

        # This is the time it has passed since last update (x).
        # We normalize it inside the 0.0 - 1.0 interval
        delta_t = float(tic - item.decay_time) / \
            host.decay_tics_to_0

        # The y is the strength that should be between 0.0 and 1.0.
        # Based on it we compute the time (x) at that point.
        # In this case they are equal.
        # prev_time = 1.0 - relation.strength

        # So we get the new time in this system of reference.
        # new_time = prev_time + delta_t

        # new_strength = 1.0 - 1.0 + relation.strength - delta_t
        # new_strength = relation.strength - delta_t

        # And, at this point, we compute the new strength.
        # Because this is linear and both go from 0 to 1
        # This is just a matter of reversing the value.
        return item.set_decay(tic, item.decay_strength - delta_t)
