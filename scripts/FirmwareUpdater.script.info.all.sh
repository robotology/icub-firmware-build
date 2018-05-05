
#!/bin/bash


# this script which uses FirmwareUpdater by means of the python program updateRobot.py

echo ""
echo ""
echo ""

echo "this bash is executing: ./updateRobot.py -t $ROBOT_CODE/robots-configuration/$ICUB_ROBOTNAME/topology.$ICUB_ROBOTNAME.xml -f ../info/firmware.info.xml -p all -a info | tee ../logs/log.of.FirmwareUpdater.$ICUB_ROBOTNAME.info.all.txt"
echo ""
./updateRobot.py -t $ROBOT_CODE/robots-configuration/$ICUB_ROBOTNAME/topology.$ICUB_ROBOTNAME.xml -f ../info/firmware.info.xml -p all -a info | tee ../logs/log.of.FirmwareUpdater.$ICUB_ROBOTNAME.info.all.txt 
echo ""
echo "this bash has executed: ./updateRobot.py -t $ROBOT_CODE/robots-configuration/$ICUB_ROBOTNAME/topology.$ICUB_ROBOTNAME.xml -f ../info/firmware.info.xml -p all -a info | tee ../logs/log.of.FirmwareUpdater.$ICUB_ROBOTNAME.info.all.txt"
echo ""
