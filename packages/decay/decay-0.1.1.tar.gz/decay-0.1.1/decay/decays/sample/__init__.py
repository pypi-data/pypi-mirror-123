# -*- coding: utf-8 -*-
"""
Contains the definition of the  class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import numpy as np

from ...kind import DecayType

logger = logging.getLogger('')


class SampleBasedDecay(DecayType):
    """
    A base class that describes the curve in terms of samples.

    Usually there will be 20 samples for which both x and y are given.
    To compute a value that falls between these two a linear interpolation
    is used.

    Implementation is expected to have two attributes:
    decay_x and decay_y
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'SampleBasedDecay()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'SampleBasedDecay()'

    def sample_count(self):
        """ Tell the number of samples in this class. """
        assert len(self.decay_x) == len(self.decay_y)
        return len(self.decay_x)

    def x_decay_interval(self, x):
        """ Get the index of an x interval based on the value of x. """
        return np.searchsorted(self.decay_x, x, side='right') - 1

    def y_decay_interval(self, y):
        """ Get the index of an y interval based on the value of y. """
        result = self.sample_count() - np.searchsorted(
            np.flip(self.decay_y), y, side='left')
        return result - 1 if result > 0 else result

    def x_decay_for_y(self, y):
        """ Compute the value of x for the given y. """
        y_interval = self.y_decay_interval(y)
        if y_interval >= self.sample_count()-1:
            return self.decay_x[self.sample_count() - 1]
        else:
            smaller_y = self.decay_y[y_interval+1]
            higher_y = self.decay_y[y_interval]
            smaller_x = self.decay_x[y_interval]
            higher_x = self.decay_x[y_interval+1]
            # (higher_y - y) / (higher_y - smaller_y) =
            #     (x - smaller_x) / (higher_x - smaller_x)
            # (higher_x - smaller_x) * (higher_y - y) /
            #     (higher_y - smaller_y) = (x - smaller_x)
            # ((higher_x - smaller_x) * (higher_y - y) /
            #     (higher_y - smaller_y)) + smaller_x = x
            x = ((higher_x - smaller_x) * (higher_y - y) /
                 (higher_y - smaller_y)) + smaller_x
            return x

    def y_decay_for_x(self, x):
        """ Compute the value of y for the given x. """
        x_interval = self.x_decay_interval(x)
        if x_interval >= self.sample_count()-1:
            return self.decay_y[self.sample_count() - 1]
        else:
            smaller_y = self.decay_y[x_interval+1]
            higher_y = self.decay_y[x_interval]
            smaller_x = self.decay_x[x_interval]
            higher_x = self.decay_x[x_interval+1]
            # (higher_y - y) / (higher_y - smaller_y) =
            #     (x - smaller_x) / (higher_x - smaller_x)
            # (higher_y - y) = (x - smaller_x) * (higher_y - smaller_y) /
            #     (higher_x - smaller_x)
            #  -y = - higher_y + (x - smaller_x) * (higher_y - smaller_y) /
            #     (higher_x - smaller_x)
            y = higher_y - (x - smaller_x) * (
                    (higher_y - smaller_y) / (higher_x - smaller_x)
            )
            return y

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
        logger.log(1, "sample based decay for item %s hosted in %s at time %r",
                   item, host, tic)

        # This is the time it has passed since last update (x).
        # We normalize it inside the 0.0 - 1.0 interval
        delta_t = float(tic - item.decay_time) / \
            host.decay_tics_to_0

        # The y is the strength that should be between 0.0 and 1.0.
        # Based on it we compute the time (x) at that point.
        prev_time = self.x_decay_for_y(item.decay_strength)

        # So we get the new time in this system of reference.
        new_time = prev_time + delta_t

        # And, at this point, we compute the new strength.
        return item.set_decay(tic, self.y_decay_for_x(new_time))
