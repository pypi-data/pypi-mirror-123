# -*- coding: utf-8 -*-
"""
Contains the definition of the DecayType class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('decay.type')


class DecayType(object):
    """
    This class represents the base for all kinds of decays.

    This class require the implementation to
    have am `update_decay()` method and to name the decay.

    Attributes:
        decay_name (str):
            a unique name for this type of decay
    """

    def __init__(self, decay_name, *args, **kwargs):
        """
        Constructor.

        Arguments:
            decay_name (str):
                a unique name for this type of decay
        """
        super().__init__(*args, **kwargs)
        self.decay_name = decay_name

    def __str__(self):
        """ Represent this object as a human-readable string. """
        raise NotImplementedError

    def __repr__(self):
        """ Represent this object as a python constructor. """
        raise NotImplementedError

    def update_decay(self, item, host, tic):
        """
        Change the value of the strength based on the time passed since the
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
        raise NotImplementedError

    @property
    def decay_type_id(self):
        """ Returns a numeric id of this type. """
        from .registry import Registry
        return Registry.instance().name_to_id[self.decay_name]
