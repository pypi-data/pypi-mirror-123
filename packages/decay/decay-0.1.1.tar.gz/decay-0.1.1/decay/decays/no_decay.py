# -*- coding: utf-8 -*-
"""
Contains the definition of the NoDecay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from decay.kind import DecayType

logger = logging.getLogger('decay.none')


class NoDecay(DecayType):
    """
    This is a decay placeholder that does not change the strength.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(decay_name='.decay.none.', *args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'NoDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'NoDecay()'

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
        logger.log(1, "no-op decay for item %s hosted in %s at time %r",
                   item, host, tic)
        return item.decay_strength
