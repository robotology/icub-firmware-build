
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""
echo "This script is about to install the 2foc-special.hex FW binary with the HW FAULT on overheating disabled on all 2FOC boards of $YARP_ROBOT_NAME"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

echo "Starting the 2FOC update with 2foc-special.hex..."


echo "this bash is executing: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME-2foc-special.xml` -f ../info/firmware.info.xml -p all -b foc-special -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc-special.update.all.foc-special.txt"
echo ""
./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME-2foc-special.xml | grep ^\".*$ | sed 's/"//g'` -f ../info/firmware.info.xml -p all -b foc-special -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc-special.update.all.foc-special.txt 
echo ""
echo "this bash has executed: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME-2foc-special.xml` -f ../info/firmware.info.xml -p all -b foc-special -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc-special.update.all.foc-special.txt"
echo ""
