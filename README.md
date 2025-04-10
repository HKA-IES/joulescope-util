# Joulescope Utilities

![Python](https://img.shields.io/badge/python-3.13-blue.svg)

Various functions to facilitate the use of the Joulescope for characterization 
of the power consumption of embedded systems.

## Requirements
- Linux Mint 22
  - May work with other distributions, not tested.
- Python 3.13
  - May work with other versions, not tested.
- Joulescope JS220
  - May work with JS110, not tested.

## Install it from the repository

```
pip install git+https://github.com/HKA-IES/joulescope-util
```

Note: The package will be eventually added to PyPi.

## Usage

```
from joulescopeutil import Joulescope

joulescope = Joulescope(trigger_gpi=0,
                        sampling_frequency=1000000,
                        gpio_voltage="3.3V")

joulescope.capture_to_file(file="joulescope_data.jls",
                           duration=4)
regions = joulescope.get_regions_statistics(file="joulescope_data.jls")
```

## Development

For bug fixing, you can raise an issue and/or implement the fix yourself.
For new features, please create an issue first to discuss it. We want to keep
this package lean.

## License
This project is licensed under the MIT License.

Developed by Jonathan Larochelle (2025) @ Laboratory for Intelligent Embedded Systems, Karlsruhe University of Applied Sciences.
