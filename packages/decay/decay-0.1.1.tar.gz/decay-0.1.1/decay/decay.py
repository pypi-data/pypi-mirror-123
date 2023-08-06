# -*- coding: utf-8 -*-
"""
Contains the definition of the Decay class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from .item import DecayItem
from .host import DecayHost

logger = logging.getLogger('Decay')


class Decay(DecayHost, DecayItem):
    """
    An item who'se strength decays over time.

    This is the "batteries included" version.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments are passed to implementation classes.
        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Decay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Decay()'
