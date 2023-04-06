# iCub Firmware Builds

This repository contains builds of the firmware for the low level boards of the [iCub robot](http://icub.org/).
The firmwares are obtained compiling the source code in [icub-firmware](https://github.com/robotology/icub-firmware) and [icub-firmware-shared](https://github.com/robotology/icub-firmware-shared) using board-specific tools.

For more information on how to upload this firmwares to the boards in the iCub robot, please see the [iCub wiki page on Firmware](http://wiki.icub.org/wiki/Firmware).

## Firmware Versioning Table

The information of which version of each release of icub-firmware-build (and corresponding [distro release](https://icub-tech-iit.github.io/documentation/sw_versioning_table/) ) correspond to each firmware version is contained in the `info/firmware.info.xml` file. The following table provide contain links to this file in the different releases, to quickly access it.

| [Distro](https://icub-tech-iit.github.io/documentation/sw_versioning_table/) | `icub-firmware-build` | `info/firmware.info.xml` |
|:----------------------------------------------------------------------------:|:---------------------:|:-------:|
| `v2023.02.2`                                                                   | `v1.34.1`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.34.1/info/firmware.info.xml) |
| `v2023.02.0`                                                                   | `v1.33.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.33.0/info/firmware.info.xml) |
| `v2022.11.0`                                                                   | `v1.29.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.29.0/info/firmware.info.xml) |
| `v2022.08.1`                                                                   | `v1.27.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.27.0/info/firmware.info.xml) |
| `v2022.08.0`                                                                   | `v1.26.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.26.0/info/firmware.info.xml) |
| `v2022.05.2`                                                                   | `v1.25.1`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.25.1/info/firmware.info.xml) |
| `v2022.05.0`                                                                   | `v1.25.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.25.0/info/firmware.info.xml) |
| `v2022.02.0`                                                                   | `v1.24.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.24.0/info/firmware.info.xml) |
| `v2021.11.1`                                                                   | `v1.23.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.23.0/info/firmware.info.xml) |
| `v2021.11.0`                                                                   | `v1.22.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.22.0/info/firmware.info.xml) |
| `v2021.08`                                                                   | `v1.21.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.21.0/info/firmware.info.xml) |
| `v2021.05`                                                                   | `v1.20.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.20.0/info/firmware.info.xml) |
| `v2021.02`                                                                   | `v1.19.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.19.0/info/firmware.info.xml) |
| `v2020.11`                                                                   | `v1.18.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.18.0/info/firmware.info.xml) |
| `v2020.08`                                                                   | `v1.17.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.17.0/info/firmware.info.xml) |
| `v2020.05`                                                                   | `v1.16.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.16.0/info/firmware.info.xml) |
| `v2020.02`                                                                   | `v1.15.0`             |  [`info/firmware.info.xml`](https://github.com/robotology/icub-firmware-build/blob/v1.15.0/info/firmware.info.xml) |

## Maintainers
This repository is maintained by:

| | |
|:---:|:---:|
| [<img src="https://github.com/marcoaccame.png" width="40">](https://github.com/marcoaccame) | [@marcoaccame](https://github.com/marcoaccame) |
