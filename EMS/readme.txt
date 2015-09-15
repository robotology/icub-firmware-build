
The folder organization is as follows:

--EMS
    |--bin                  contains the binaries to be loaded in the partitions of the EMS board.
    |    |
    |    |--application     contains the ems application
    |    |
    |    |--environment     contains the loader, updater, maintainer, EEPROM eraser and other programs.
    |
    |
    |--scripts              contains scripts to be used to load the binaries in the EMS board.
                            for instance: to burn the loader and updater in FLASH using the JTAG.
                            