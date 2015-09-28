
The folder organization is as follows:

--MC4PLUS
    |--bin                  contains the binaries to be loaded in the partitions of the MC4PLUS board.
    |    |
    |    |--application     contains the mc4plus application
    |    |
    |    |--environment     contains the loader, updater, maintainer, EEPROM eraser and other programs.
    |
    |
    |--scripts              contains scripts to be used to load the binaries in the MC4PLUS board.
                            for instance: to burn the loader and updater in FLASH using the JTAG.
                            