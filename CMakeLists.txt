# SPDX-FileCopyrightText: Fondazione Istituto Italiano di Tecnologia (IIT)
# SPDX-License-Identifier: BSD-3-Clause

cmake_minimum_required(VERSION 3.0...3.28)

project(icub-firmware)

include(GNUInstallDirs)

set(ICUB_FIRMWARE_INSTALL_ROOT ${CMAKE_INSTALL_DATAROOTDIR}/icub-firmware)

install(DIRECTORY CAN DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
install(DIRECTORY ETH DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
install(DIRECTORY info DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})
install(DIRECTORY logs DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT})

# The scripts installed in scripts folder need to be installed with a bit of care.
# First of all, they should be installed with executable permissions, then a
# redirect script is installed in ${CMAKE_INSTALL_BINDIR},
# to permit to invoke the scripts as any  other script, while the original script
# is installed in ${ICUB_FIRMWARE_INSTALL_ROOT} to preserve the relative paths
# between the scripts and the used files that are the one used in the scripts
file(GLOB bash_scripts ${CMAKE_CURRENT_SOURCE_DIR}/scripts/*.sh)
file(GLOB py_scripts ${CMAKE_CURRENT_SOURCE_DIR}/scripts/*.py)

# Python scripts are directly installed in ${ICUB_FIRMWARE_INSTALL_ROOT}/scripts,
# as they are not invoked directly by the user
foreach(py_script ${py_scripts})
    install(PROGRAMS ${script} DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT}/scripts)
endforeach()

# Bash scripts are directly installed in ${ICUB_FIRMWARE_INSTALL_ROOT}/scripts,
# and a redirect script is installed in ${CMAKE_INSTALL_BINDIR} with a redirect
# to the actual script
foreach(bash_script ${bash_scripts})
    # Original script
    install(PROGRAMS ${bash_script} DESTINATION ${ICUB_FIRMWARE_INSTALL_ROOT}/scripts)

    # Generate redirect script
    file(RELATIVE_PATH ICUB_FIRMWARE_RELATIVE_PATH_BETWEEN_BIN_AND_ICUB_FIRMWARE_SCRIPTS 
                       ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}
                       ${CMAKE_INSTALL_PREFIX}/${ICUB_FIRMWARE_INSTALL_ROOT}/scripts)
    get_filename_component(ICUB_FIRMARE_BASH_SCRIPT_NAME ${bash_script} NAME)
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/scripts/FirmwareUpdater.script.redirect.sh.in
                   ${CMAKE_CURRENT_BINARY_DIR}/${ICUB_FIRMARE_BASH_SCRIPT_NAME})
    install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/${ICUB_FIRMARE_BASH_SCRIPT_NAME} DESTINATION ${CMAKE_INSTALL_BINDIR})
endforeach()

