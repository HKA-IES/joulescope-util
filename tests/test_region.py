# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pytest
import numpy as np

# import your own module
from joulescopeutil import Region


class TestRegion:
    def test_init(self):
        """
        When Region is initialized with valid parameters,
        - all attributes are calculated as expected.
        """
        # Test values taken from
        # https://en.wikipedia.org/wiki/Standard_deviation, because they yield
        # nice average and standard deviation values.
        duration = 14
        voltage_values = np.array([2., 4., 4., 4., 5., 5., 7., 9.])
        current_values = voltage_values * 10
        power_values = voltage_values * 100

        expected_duration = 14
        expected_voltage_avg = 5.
        expected_voltage_stdev = 2.
        expected_voltage_min = 2.
        expected_voltage_max = 9.
        expected_current_avg = 5. * 10
        expected_current_stdev = 2. * 10
        expected_current_min = 2. * 10
        expected_current_max = 9. * 10
        expected_power_avg = 5. * 100
        expected_power_stdev = 2. * 100
        expected_power_min = 2. * 100
        expected_power_max = 9. * 100
        expected_energy = expected_power_avg * expected_duration

        region = Region(duration, voltage_values, current_values, power_values)

        assert region.duration == pytest.approx(expected_duration)
        assert region.voltage_avg == pytest.approx(expected_voltage_avg)
        assert region.voltage_stdev == pytest.approx(expected_voltage_stdev)
        assert region.voltage_min == pytest.approx(expected_voltage_min)
        assert region.voltage_max == pytest.approx(expected_voltage_max)
        assert region.current_avg == pytest.approx(expected_current_avg)
        assert region.current_stdev == pytest.approx(expected_current_stdev)
        assert region.current_min == pytest.approx(expected_current_min)
        assert region.current_max == pytest.approx(expected_current_max)
        assert region.power_avg == pytest.approx(expected_power_avg)
        assert region.power_stdev == pytest.approx(expected_power_stdev)
        assert region.power_min == pytest.approx(expected_power_min)
        assert region.power_max == pytest.approx(expected_power_max)
        assert region.energy == pytest.approx(expected_energy)
