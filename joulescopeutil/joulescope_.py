# -*- coding: utf-8 -*-

# import built-in module
import time
from typing import BinaryIO
import warnings

# import third-party modules
import joulescope
from joulescope.data_recorder import DataRecorder, DataReader
import numpy as np
import scipy

# import your own module
from .region import Region

import logging
logger = logging.getLogger(__name__)



class Joulescope:
    """
    Controls a Joulescope device.
    """

    def __init__(self, trigger_gpi: int = 0,
                 sampling_frequency: int = 1000000,
                 gpio_voltage: str = "1.8V"):
        """
        Initialize a Joulescope device.

        Only one device should be connected.

        Only tested with JS220.

        Parameters
        ----------
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
        self._device = joulescope.scan_require_one(config='auto')
        self._device.open()
        self.disable_power_to_dut()

        self.sampling_frequency = sampling_frequency
        self.trigger_gpi = trigger_gpi

        self._device.parameter_set("io_voltage", gpio_voltage)

    def enable_power_to_dut(self) -> None:
        """
        Enables power to device under test.
        """
        self._device.parameter_set("i_range", "auto")

    def disable_power_to_dut(self) -> None:
        """
        Disables power to device under test.
        """
        self._device.parameter_set("i_range", "off")

    def capture_to_file(self, file: str | BinaryIO, duration: float) -> None:
        """
        Capture Joulescope data to specified file.

        Parameters
        ----------
        file : str
            file name or file handle.
        duration: float
            time to capture in seconds. Values below 4 seconds are set to 4
            because we have observed errors in the generated files for shorter
            durations. No idea if the duration is really the root cause, but it
            seems to help.
        """
        if duration < 4:
            # Note: very tacky fix, because I observed sometimes for shorter
            # durations errors in the generated .jls files. Have no idea if
            # the duration is really the root cause, but it seems to help.
            duration = 4
            logger.warning(f"Duration increased to 4 seconds to prevent errors "
                          f"in the file.")
        logger.debug(f"Capturing to file {file}.")
        recorder = DataRecorder(file, calibration=self._device.calibration)
        self._device.stream_process_register(recorder)
        self.disable_power_to_dut()
        t_stop = time.time() + duration
        self._device.start(duration=duration)
        self.enable_power_to_dut()

        while True:
            time.sleep(0.01)
            if t_stop and time.time() > t_stop:
                break

        self._device.stop()
        recorder.close()
        self._device.stream_process_unregister(recorder)
        logger.debug(f"Capturing complete.")

    def get_regions_statistics(self, file: str | BinaryIO) -> list[Region]:
        """
        Compute statistics for the regions detected in a given Joulescope
        recording.

        Regions are indicated by a high trigger level.

        Parameters
        ----------
        file : str
            file name or file handle.
        """
        reader = DataReader()
        reader.open(file)
        data = reader.samples_get()

        # Identify rising and falling edges in the signal
        if self.trigger_gpi == 0:
            trigger_signal = "current_lsb"
        elif self.trigger_gpi == 1:
            trigger_signal = "voltage_lsb"
        trigger_data = data["signals"][trigger_signal]["value"]
        trigger_data = trigger_data.astype(np.int8)
        trigger_data_diff = np.diff(trigger_data)

        del trigger_data

        rising_edges, _ = scipy.signal.find_peaks(trigger_data_diff)
        falling_edges, _ = scipy.signal.find_peaks(-trigger_data_diff)

        del trigger_data_diff

        nb_regions = np.min([len(rising_edges), len(falling_edges)])
        logger.debug(f"Found {nb_regions} regions.")

        rising_edges = rising_edges[-nb_regions:]
        falling_edges = falling_edges[-nb_regions:]

        regions = []

        for i in range(nb_regions):
            start = rising_edges[i]
            end = falling_edges[i]
            region_duration = (end - start) / self._sampling_frequency
            regions.append(Region(region_duration,
                                           data["signals"]["voltage"]["value"][
                                           start:end],
                                           data["signals"]["current"]["value"][
                                           start:end],
                                           data["signals"]["power"]["value"][
                                           start:end]))

        return regions

    def __del__(self):
        self._device.close()

    @property
    def sampling_frequency(self) -> int:
        return self._device.sampling_frequency

    @sampling_frequency.setter
    def sampling_frequency(self, value: int):
        """
        Should be one of[2000000, 1000000, 500000, 200000, 100000, 50000, 20000,
         10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10]
        """
        try:
            self._device.parameter_set("sampling_frequency",
                                       value)
            self._sampling_frequency = value
        except KeyError:
            raise ValueError(f"Invalid sampling_frequency={value}.")

    @property
    def trigger_gpi(self) -> int:
        return self._trigger_gpi

    @trigger_gpi.setter
    def trigger_gpi(self, value: int):
        if value not in [0, 1]:
            raise ValueError(f"Trigger GPI should be 0 or 1.")

        self._trigger_gpi = value

    @property
    def power_to_dut_enabled(self) -> bool:
        """
        Is power to device under test enabled?
        """
        if self._device.parameter_get("i_range") == "off":
            return False
        else:
            return True
