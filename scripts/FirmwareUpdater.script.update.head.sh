
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""

echo "this bash is executing: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.xml` -f ../info/firmware.info.xml -p head -a update | tee ../logs/log.of.FirmwareUpdater.$YARP_ROBOT_NAME.update.head.txt"
echo ""
./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.xml` -f ../info/firmware.info.xml -p head -a update | tee ../logs/log.of.FirmwareUpdater.$YARP_ROBOT_NAME.update.head.txt 
echo ""
echo "this bash has executed: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.xml` -f ../info/firmware.info.xml -p head -a update | tee ../logs/log.of.FirmwareUpdater.$YARP_ROBOT_NAME.update.head.txt"
echo ""
