# SPDX-FileCopyrightText: Fondazione Istituto Italiano di Tecnologia (IIT)
# SPDX-License-Identifier: BSD-3-Clause

cmake_minimum_required(VERSION 3.0...3.28)

project(icub-firmware)

include(GNUInstallDirs)

set(ICUB_FIRMWARE_INSTALL_ROOT ${CMAKE_INSTALL_DATAROOTDIR}/icub-firmware)

install(DIRECTORY CAN DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
install(DIRECTORY ETH DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
install(DIRECTORY info DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
install(DIRECTORY scripts DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
