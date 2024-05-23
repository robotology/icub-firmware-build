
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""
echo "This script is about to install the standard 2foc.hex FW binary on all 2FOC boards of $YARP_ROBOT_NAME"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

echo "Starting the 2FOC update with 2foc.hex..."

echo "this bash is executing: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.2foc.xml` -f ../info/firmware.info.xml -p all -b foc -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc..update.all.foc.txt"
echo ""
./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.2foc.xml | grep ^\".*$ | sed 's/"//g'` -f ../info/firmware.info.xml -p all -b foc -a update | tee ../logs/log.of.FirmwareUpdater..ergocub-2foc.update.all.foc.txt 
echo ""
echo "this bash has executed: ./manageFWrobot.py -n `yarp resource --from network.$YARP_ROBOT_NAME.2foc.xml` -f ../info/firmware.info.xml -p all -b foc -a update | tee ../logs/log.of.FirmwareUpdater..ergocub-2foc.update.all.foc.txt"
echo ""
