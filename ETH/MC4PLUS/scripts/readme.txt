
in order to use these scripts you must have keil uv5 installed. even without a valid licence. you also must have a ulink-pro (ulink-2) programming device. 

use these scripts to:

1.  erase the eeprom and the flash of the ems.
    a. attach a ulink-pro (ulink-2) to the board.
    b. power the board on
    c. launch erase-eeprom.bat which will load a small program in the first partition.
    d. power the board off and then on. the loaded program will erase the first 8KB of eeprom and the whole flash.
       if operation is successful, the first two leds (red and yellow) will blink in an alternate way at 1 hz,
       in case of failure the led will not blink at all or will blink at 10 hz.
       
       
2.  burn the loader program in the first partition of the ems.
    a. attach a ulink-pro (ulink-2) to the board.
    b. power the board on
    c. launch burn-loader.bat which will load the loader program into the first partition.
    d. power the board off and then on. 
       the loaded program will force the eeprom to contain a valid partition table. then will try to launch programs in the second or third partition.
       if nothing is found, as it is the case after the use of erase-eeprom-flash.bat script, then the loader will enter in a wild blink at 20 hz of all its leds.
    
3.  burn the updater program in the second partition of the ems.
    a. attach a ulink-pro (ulink-2) to the board.
    b. power the board on
    c. launch burn-updater.bat which will load the updater program into the second partition.
    d. power the board off and then on. 
       the loader will load this program, which will make all leds blink at 1 hz. after 5 seconds the updater will instead blink at 2 hz.
       the updater is programmed to respond to the FirmwareUpdater at address 10.0.1.99
       any further operations must be done using the FirmwareUpdater. 