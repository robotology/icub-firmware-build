
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program manageFWrobot.py

echo ""
echo ""
echo ""
echo "this script is about to install ..... "
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

echo "If I'm here means the user wants to proceed"


echo "this bash is executing: ./manageFWrobot.py -n `yarp resource --from network.ergocub-2foc-special.xml` -f ../info/firmware.info.xml -p all -b foc-special -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc-special.update.all.foc-special.txt"
echo ""
./manageFWrobot.py -n `yarp resource --from network.ergocub-2foc-special.xml | grep ^\".*$ | sed 's/"//g'` -f ../info/firmware.info.xml -p all -b foc-special -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc-special.update.all.foc-special.txt 
echo ""
echo "this bash has executed: ./manageFWrobot.py -n `yarp resource --from network.ergocub-2foc-special.xml` -f ../info/firmware.info.xml -p all -b foc-special -a update | tee ../logs/log.of.FirmwareUpdater.ergocub-2foc-special.update.all.foc-special.txt"
echo ""
