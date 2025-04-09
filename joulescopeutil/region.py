# -*- coding: utf-8 -*-

# import built-in module
import dataclasses

# import third-party modules
import numpy as np

# import your own module


@dataclasses.dataclass(init=False)
class Region:
    """
    Contains statistics for a region, also called a time period.

    Attributes
    ----------
    # TODO: Documentation of attributes
    """

    duration: float         # s

    voltage_avg: float      # V
    voltage_stdev: float    # V
    voltage_min: float      # V
    voltage_max: float      # V

    current_avg: float      # A
    current_stdev: float    # A
    current_min: float      # A
    current_max: float      # A

    power_avg: float        # W
    power_stdev: float      # W
    power_min: float        # W
    power_max: float        # W

    energy: float           # J

    def __init__(self, duration: float, voltage_values: np.ndarray, current_values: np.ndarray, power_values: np.ndarray):
        """
        Initialize a Region object from the duration (in seconds) and arrays of measured voltage, current, and power.
        The energy during the region is the average power multiplied by the duration.

        Parameters
        ----------
        # TODO: Documentation of function.
        """
        self.duration = float(duration)

        self.voltage_avg = float(np.average(voltage_values))
        self.voltage_stdev = float(np.std(voltage_values))
        self.voltage_min = float(np.min(voltage_values))
        self.voltage_max = float(np.max(voltage_values))

        self.current_avg = float(np.average(current_values))
        self.current_stdev = float(np.std(current_values))
        self.current_min = float(np.min(current_values))
        self.current_max = float(np.max(current_values))

        self.power_avg = float(np.average(power_values))
        self.power_stdev = float(np.std(power_values))
        self.power_min = float(np.min(power_values))
        self.power_max = float(np.max(power_values))

        self.energy = self.power_avg * self.duration