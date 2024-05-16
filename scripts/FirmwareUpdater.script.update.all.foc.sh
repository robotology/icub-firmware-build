
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""

echo "this bash is executing: ./manageFWrobot.py -n `yarp resource --from network.ergocub-2foc.xml` -f ../info/firmware.info.xml -p all -b foc -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc..update.all.foc.txt"
echo ""
./manageFWrobot.py -n `yarp resource --from network.ergocub-2foc.xml | grep ^\".*$ | sed 's/"//g'` -f ../info/firmware.info.xml -p all -b foc -a update | tee ../logs/log.of.FirmwareUpdater..ergocub-2foc.update.all.foc.txt 
echo ""
echo "this bash has executed: ./manageFWrobot.py -n `yarp resource --from network.ergocub-2foc.xml` -f ../info/firmware.info.xml -p all -b foc -a update | tee ../logs/log.of.FirmwareUpdater..ergocub-2foc.update.all.foc.txt"
echo ""
