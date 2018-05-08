
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""

echo "this bash is executing: ./manageFWrobot.py -n $ROBOT_CODE/robots-configuration/$ICUB_ROBOTNAME/network.$ICUB_ROBOTNAME.xml -f ../info/firmware.info.xml -p all -a update | tee ../logs/log.of.FirmwareUpdater.$ICUB_ROBOTNAME.update.all.txt"
echo ""
./manageFWrobot.py -n $ROBOT_CODE/robots-configuration/$ICUB_ROBOTNAME/network.$ICUB_ROBOTNAME.xml -f ../info/firmware.info.xml -p all -a update | tee ../logs/log.of.FirmwareUpdater.$ICUB_ROBOTNAME.update.all.txt 
echo ""
echo "this bash has executed: ./manageFWrobot.py -n $ROBOT_CODE/robots-configuration/$ICUB_ROBOTNAME/network.$ICUB_ROBOTNAME.xml -f ../info/firmware.info.xml -p all -a update | tee ../logs/log.of.FirmwareUpdater.$ICUB_ROBOTNAME.update.all.txt"
echo ""
