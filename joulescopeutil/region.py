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
    duration: float
        Duration of the region in seconds.
    voltage_avg: float
        Average voltage during the region in volts.
    voltage_stdev: float
        Standard deviation of voltage during the region in volts.
    voltage_min: float
        Minimum voltage during the region in volts.
    voltage_max: float
        Maximum voltage during the region in volts.
    current_avg: float
        Average current during the region in amperes.
    current_stdev: float
        Standard deviation of current during the region in amperes.
    current_min: float
        Minimum current during the region in amperes.
    current_max: float
        Maximum current during the region in amperes.
    power_avg: float
        Average power during the region in watts.
    power_stdev: float
        Standard deviation of power during the region in watts.
    power_min: float
        Minimum power during the region in watts.
    power_max: float
        Maximum power during the region in watts.
    energy: float
        Energy during the region in joules.
    """

    duration: float

    voltage_avg: float
    voltage_stdev: float
    voltage_min: float
    voltage_max: float

    current_avg: float
    current_stdev: float
    current_min: float
    current_max: float

    power_avg: float
    power_stdev: float
    power_min: float
    power_max: float

    energy: float

    def __init__(self, duration: float, voltage_values: np.ndarray,
                 current_values: np.ndarray, power_values: np.ndarray):
        """
        Initialize a Region object from the duration (in seconds) and arrays of
        measured voltage, current, and power. The energy during the region is
        the average power multiplied by the duration.

        Parameters
        ----------
        duration: float
            Duration of the region in seconds.
        voltage_values: np.ndarray
            Array of voltage values during the region in volts.
        current_values: np.ndarray
            Array of current values during the region in amperes.
        power_values: np.ndarray
            Array of power values during the region in watts.
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
