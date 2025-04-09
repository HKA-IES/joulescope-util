# -*- coding: utf-8 -*-

# import built-in module
import dataclasses
import time

# import third-party modules
import joulescope
from joulescope.data_recorder import DataRecorder, DataReader
import numpy as np
import scipy

# import your own module
from region import Region

import logging
logger = logging.getLogger(__name__)



class Joulescope:
    """
    Controls a Joulescope JS220 device.
    """

    def __init__(self, trigger_gpio: str = "gpi[0]",
                 sampling_frequency: int = 1000000):
        """
        :param trigger_gpio: gpi[0] or gpi[1], whichever should be used to
        indicate intervals.
        :param sampling_frequency:
        """
        self._device = joulescope.scan_require_one(config='auto')
        self._device.open()
        self.disable_power_to_dut()

        self.sampling_frequency = sampling_frequency
        self.trigger_gpio = trigger_gpio

        # TODO: Make sure below is more robust
        self._device.parameter_set("io_voltage", "1.8V")

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

    def capture_to_file(self, file, duration) -> None:
        """
        Capture Joulescope data to specified file.

        :param file: file name or file handle.
        :param duration: time to capture in seconds.
        """
        if duration < 4:
            # Note: very tacky fix, because I observed sometimes for shorter
            # durations errors in the generated .jls files. Have no idea if
            # the duration is really the root cause, but it seems to help.
            duration = 4
        # logger.debug(f"Capturing to file {file}.")
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

    def get_intervals_statistics(self, file, nb_intervals_expected = None) -> list[Region]:
        """
        Compute statistics for the intervals detected in a given Joulescope
        recording.
        :param file: file name or file handle.
        """
        reader = DataReader()
        reader.open(file)
        data = reader.samples_get()

        # Identify rising and falling edges in the signal
        trigger_data = data["signals"][self._trigger_signal]["value"]
        trigger_data = trigger_data.astype(np.int8)
        trigger_data_diff = np.diff(trigger_data)

        del trigger_data

        rising_edges, _ = scipy.signal.find_peaks(trigger_data_diff)
        falling_edges, _ = scipy.signal.find_peaks(-trigger_data_diff)

        del trigger_data_diff

        nb_intervals = np.min([len(rising_edges), len(falling_edges)])
        logger.debug(f"Found {nb_intervals} intervals.")

        if nb_intervals_expected is not None:
            if nb_intervals_expected > nb_intervals:
                raise RuntimeError(f"We expect {nb_intervals_expected} "
                                   f"intervals, but we measured {nb_intervals}"
                                   f" intervals.")

        rising_edges = rising_edges[-nb_intervals:]
        falling_edges = falling_edges[-nb_intervals:]

        intervals = []

        for i in range(nb_intervals):
            start = rising_edges[i]
            end = falling_edges[i]
            interval_duration = (end - start) / self._sampling_frequency
            intervals.append(Region(interval_duration,
                                           data["signals"]["voltage"]["value"][
                                           start:end],
                                           data["signals"]["current"]["value"][
                                           start:end],
                                           data["signals"]["power"]["value"][
                                           start:end]))

        return intervals

    def __del__(self):
        self._device.close()

    @property
    def sampling_frequency(self) -> int:
        return self._device.sampling_frequency

    @sampling_frequency.setter
    def sampling_frequency(self, value: int):
        try:
            self._device.parameter_set("sampling_frequency",
                                       value)
            self._sampling_frequency = value
        except KeyError:
            raise ValueError(f"Invalid sampling_frequency={value}.")

    @property
    def trigger_gpio(self) -> str:
        return self._trigger_gpio

    @trigger_gpio.setter
    def trigger_gpio(self, value: str):
        if value == "gpi[0]":
            self._trigger_gpio = value
            self._trigger_signal = "current_lsb"
        elif value == "gpi[1]":
            self._trigger_gpio = value
            self._trigger_signal = "voltage_lsb"
        else:
            raise ValueError(f"Bad trigger signal {value}, should be either "
                             f"gpi[0] or gpi[1].")

    @property
    def power_to_dut_enabled(self) -> bool:
        """
        Is power to device under test enabled?
        """
        if self._device.parameter_get("i_range") == "off":
            return False
        else:
            return True


if __name__ == '__main__':
    import tempfile
    import os

    # Parameters
    GPIO = "gpi[0]"

    # Script begin
    joulescope = Joulescope(GPIO)
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    joulescope.capture_to_file("joulescope_recording_test.jls", 1)
    intervals = joulescope.get_intervals_statistics("joulescope_recording_test.jls")
    tmp_file.close()
    os.unlink(tmp_file.name)

    for interval in intervals:
        print(interval)

    del joulescope

    # Script end
