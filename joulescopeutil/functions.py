# -*- coding: utf-8 -*-

# import built-in module
from typing import BinaryIO

# import third-party modules

# import your own module
from .region import Region
from .joulescope_ import Joulescope


def get_regions_statistics(file: str | BinaryIO, duration: float = 4.,
                           trigger_gpi: int = 0,
                           sampling_frequency: int = 1000000,
                           gpio_voltage: str = "3.3V") -> list[Region]:
    """
    Compute statistics for the regions identified by a high trigger level on
    pin trigger_gpi.

    Parameters
    ----------
    file : str
        file name or file handle.
    duration: float
        time to capture in seconds. Values below 4 seconds are set to 4
        because we have observed errors in the generated files for shorter
        durations. No idea if the duration is really the root cause, but it
        seems to help.
    trigger_gpi : int
        General purpose input to use as trigger for the energy measurements.
        Should be 0 or 1.
    sampling_frequency: int
        Sampling frequency in Hertz. Should be one of [2000000, 1000000,
        500000, 200000, 100000, 50000, 20000, 10000, 5000, 2000, 1000, 500,
        200, 100, 50, 20, 10]
    gpio_voltage: float
        One of ["1.8V", "2.1V", "2.5V", "2.7V", "3.0V", "3.3V", "3.6V",
        "5.0V"]
    """
    joulescope = Joulescope(trigger_gpi, sampling_frequency, gpio_voltage)
    joulescope.capture_to_file(file, duration)
    regions = joulescope.get_regions_statistics(file)
    return regions
