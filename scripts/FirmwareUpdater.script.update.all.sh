
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""
echo "This script is about to install the standard FW binary on all the boards of $YARP_ROBOT_NAME"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1


echo "this bash is executing: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.xml` -f ../info/firmware.info.xml -p all -a update | tee ../logs/log.of.FirmwareUpdater.$YARP_ROBOT_NAME.update.all.txt"
echo ""
./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.xml | grep ^\".*$ | sed 's/"//g'` -f ../info/firmware.info.xml -p all -a update | tee ../logs/log.of.FirmwareUpdater.$YARP_ROBOT_NAME.update.all.txt
echo ""
echo "this bash has executed: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.xml` -f ../info/firmware.info.xml -p all -a update | tee ../logs/log.of.FirmwareUpdater.$YARP_ROBOT_NAME.update.all.txt"
echo ""
