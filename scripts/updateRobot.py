#!/usr/bin/python


# Copyright (C) 2018 iCub Facility - Istituto Italiano di Tecnologia
# Author:  Marco Accame
# email:   marco.accame@iit.it
# website: www.robotcub.org
# Permission is granted to copy, distribute, and/or modify this program
# under the terms of the GNU General Public License, version 2 or any
# later version published by the Free Software Foundation.
#
# A copy of the license can be found at
# http://www.robotcub.org/icub/license/gpl.txt
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details


# description:
# this script is a front-end for the FirmwareUpdater program in non GUI mode. it performs automatic firmware updates on robots.

import os


# it retrieves properties of a given board
def get_board_properties(boardroot, brdtype):
    prop = {}

    for p in boardroot.findall('board'):
        if brdtype == p.get('type'):
            prop = p
    return prop
# end of: def


# it retrieves the address of a board in string form
def from_board_to_stringofaddress(brd):
    adr = brd.find('ataddress').attrib
    ss = adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')
    return ss
# end of: def

# it retrieves the firmwar version of a board in string form
def from_firmware_to_stringofversion(fw):
    ss = fw.find('version').get('major', '0') + '.' + fw.find('version').get('minor', '0') + '.' + fw.find('version').get('build', '0')
    return ss
# end of: def

# FirmwareUpdater --nogui --force-eth-maintenance --device ETH --id eth1 --eth_board $ipaddress --verbosity $verbosity
# FirmwareUpdater --nogui --force-eth-application --device ETH --id eth1 --eth_board $ipaddress --verbosity $verbosity
# FirmwareUpdater --nogui --program --device ETH --id eth1 --eth_board $ipaddress --file ${mapofboards[$boardtag]} --verbosity $verbosity
# FirmwareUpdater --nogui --program --device ETH --id eth1 --eth_board $ipaddress --can_line $canline --can_id $canid --file ${mapofboards[$boardtag]} --verbosity $verbosity


# it send eth board in maintenance by calling the external program
def eth_force_maintenance(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
 
    command = 'FirmwareUpdater --nogui --force-eth-maintenance --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip') + ' --verbosity ' + str(_verbosityFU)

    if _verbose > 1:
        print 'eth_force_maintenance(): sending eth board in maintenance mode w/ command:'
        print command

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    if 0 != r:
        print 'eth_force_maintenance(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip')
        return r   

    return r
# end of: def eth_force_maintenance():


# it send eth board in application by calling the external program
def eth_force_application(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')

    command = 'FirmwareUpdater --nogui --force-eth-application --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip') + ' --verbosity ' + str(_verbosityFU)
 
    if _verbose > 1:
        print 'eth_force_application(): sending eth board in application mode w/ command:'
        print command

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    if 0 != r:
        print 'eth_force_application(): FAILURE sending in application mode eth board @ ' + adr.get('ip')
        return r   

    return r
# end of: def eth_force_application():

# it decides if to go to maintenance (only eth, eth:can)
def goto_maintenance(brd, prp):
    r = 1
    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = eth_force_maintenance(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = eth_force_maintenance(brd, prp)
        else:
            print 'goto_maintenance(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported'
            r = 1        
    elif 'CFW' == ondevice:
        print 'goto_maintenance(): WARNING the device ' + ondevice + ' does not need to go in maintenance mode!'   
        r = 0
    else:
        print 'goto_maintenance(): FAILURE the device ' + ondevice + ' is unsupported'
        r = 1

    return r
# end of: def

# it decides if to go to application (only eth, eth:can)
def goto_application(brd, prp):

    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = eth_force_application(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = eth_force_application(brd, prp)
        else:
            print 'goto_application(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported'
            r = 1        
    elif 'CFW' == ondevice:
        print 'goto_application(): WARNING the device ' + ondevice + ' does not need to go in application mode!'  
        r = 0  
    else:
        print 'goto_application(): FAILURE the device ' + ondevice + ' is unsupported'
        r = 1

    return r
# end of: def


# it selects what kind of fw update to do: eth, eth:can, cfw
def do_firmware_update(brd, prp):
    r = 1
    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = do_firmware_update_eth(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = do_firmware_update_canovereth(brd, prp)
        else:
            print 'do_firmware_update(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported'
            r = 1        
    elif 'CFW' == ondevice:
        r = do_firmware_update_cfw(brd, prp)
    else:
        print 'do_firmware_update(): FAILURE the device ' + ondevice + ' is unsupported'
        r = 1

    return r
# end of: def

# it performs fw update of cfw device
def do_firmware_update_cfw(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    print 'do_firmware_update_cfw(): performing fw update on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')
    print 'do_firmware_update_cfw(): FAILURE because .... python code for this  DEVICE IS not developed yet...........'
    return 1
# end of: def


# it tells how long it takes to perform fw update
def getTimeOfFirmwareUpdate(brdtype):
    r = 666

    if brdtype == 'ems4':
        r = 8
    elif brdtype == 'mc4plus':
        r = 8
    elif brdtype == 'mc2plus':
        r = 8
    elif brdtype == 'foc':
        r = 90
    elif brdtype == 'mtb':
        r = 90
    elif brdtype == 'mtb4':
        r = 270
    elif brdtype == 'mais':
        r = 45
    elif brdtype == 'strain':
        r = 60
    elif brdtype == 'strain2':
        r = 270
    elif brdtype == 'mc4':
        r = 66
    elif brdtype == 'bll':
        r = 66
    elif brdtype == 'dsp':
        r = 66
    else:
        r = 666

    return r
# end of: def


# it performs fw update of can over eth device
def do_firmware_update_canovereth(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print 'do_firmware_update_canovereth(): performing fw update on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')

    r = eth_force_maintenance(brd, prp)

    if 0 != r:
        print 'do_firmware_update_canovereth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip')
        return r   

    tmp1 = 'FirmwareUpdater --nogui --program --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --file ' + fw.find('file').text + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print 'do_firmware_update_canovereth(): uploading can firmware w/ command:'
        print command 

    if _verbose > 0:
        boardtype = brd.get('type')
        timeofupload = getTimeOfFirmwareUpdate(boardtype)
        print '  - message: please be prepared to wait for some time ... fw update of a ' + boardtype + ' typically lasts ' + str(timeofupload) + ' seconds'

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    if 0 != r:
         print 'do_firmware_update_canovereth(): FAILURE programming can board @ ' + adr.get('ip') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')
         return r 


    if _verbose > 1:
        print 'do_firmware_update_canovereth(): done!'

    return r
# end of: def


# it performs firmware update by calling the external program
def do_firmware_update_eth(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')

    if _verbose > 1:
        print 'do_firmware_update_eth(): performing fw update on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')

    r = eth_force_maintenance(brd, prp)

    if 0 != r:
        print 'do_firmware_update_eth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip')
        return r     

   
    command = 'FirmwareUpdater --nogui --program --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip') + ' --file ' + fw.find('file').text + ' --verbosity ' + str(_verbosityFU)

    if _verbose > 1:
        print 'do_firmware_update_eth(): uploading eth firmware w/ command:'        
        print command 

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    if 0 != r:
         print 'do_firmware_update_eth(): FAILURE programming eth board @ ' + adr.get('ip')
         return r 


    if _verbose > 1:
        print 'do_firmware_update_eth(): done!'

    return r
# end of: def


#print 'processing: part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)

# it prints info about a given board
def print_board_info(partname, brd, prp):
    r = 0
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')

    print 'INFO: (from xml parsing) on part = ' + partname + ': board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', device = ' + brd.find('ondevice').text + ', address = ' + from_board_to_stringofaddress(brd) + ', firmware version = ' + from_firmware_to_stringofversion(fw)

    return r
# end of: def


# update all the boards in the xml file which are inside targetpart and are targetboard
def update(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print 'processing a --update request:'

    for part in robotroot.findall('part'):
        # print part.tag, part.attrib
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print 'processing part = ' + part.get('name')
            for brd in part.findall('board'):
                prp = get_board_properties(boardroot, brd.get('type'))

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                
                    countOfFound = countOfFound + 1
                    details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)

                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print '- EXCLUSION #' + str(countOfExcluded)
                            print '  - of: ' + details

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print '- OPERATION #' + str(countOfAttempts)
                            print '  - type: firmware update'
                            print '  - target: ' + details

                        r = do_firmware_update(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)'
                            # exit()
                        elif _verbose > 0:
                            print '  - result: SUCCESS'

                    # end of: if _excl...
                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    if _verbose > 0:
        print_result('update()', countOfFound, countOfExcluded, countOfFailures)
    # end of if ...

    return 
# end of: def update

# send in maintenance all the boards in the xml file which are inside targetpart and are targetboard
def maintenance(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print 'processing a --forcemaintenance request:'

    for part in robotroot.findall('part'):
        # print part.tag, part.attrib
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print 'processing part = ' + part.get('name')
            for brd in part.findall('board'):
                prp = get_board_properties(boardroot, brd.get('type'))

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                    
                    countOfFound = countOfFound + 1
                    details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)

                    if _excludedboard == brd.get('type'):

                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print '- EXCLUSION #' + str(countOfExcluded)
                            print '  - of: ' + details

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print '- OPERATION #' + str(countOfAttempts)
                            print '  - type: force maintenance'
                            print '  - target: ' + details                  
                        
                        r = goto_maintenance(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)'
                            # exit()
                        elif _verbose > 0:
                            print '  - result: SUCCESS'

                    # end of: if _excl... 
                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    if _verbose > 0:
        print_result('maintenance()', countOfFound, countOfExcluded, countOfFailures)
    # end of if ...

    return r

# end of: def

# send in application all the boards in the xml file which are inside targetpart and are targetboard
def application(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print 'processing a --forceapplication request:'

    for part in robotroot.findall('part'):
        # print part.tag, part.attrib
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print 'processing part = ' + part.get('name')
            for brd in part.findall('board'):
                prp = get_board_properties(boardroot, brd.get('type'))

                if ('all' == targetboard) or (targetboard == brd.get('type')):

                    countOfFound = countOfFound + 1
                    details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)

                    if _excludedboard == brd.get('type'):

                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print '- EXCLUSION #' + str(countOfExcluded)
                            print '  - of: ' + details

                    else:
                    
                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print '- OPERATION #' + str(countOfAttempts)
                            print '  - type: force application'
                            print '  - target: ' + details
     
                        r = goto_application(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)'
                            # exit()
                        elif _verbose > 0:
                            print '  - result: SUCCESS'

                    # end of: if _excl... 
                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    if _verbose > 0:
        print_result('application()', countOfFound, countOfExcluded, countOfFailures)
    # end of if ...

    return r

# end of: def


# prints info of all the boards in the xml file which are inside targetpart and are targetboard
def info(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    estimatedTimeForFWupdate = 0;

    if _verbose > 1:
        print 'processing a --info request:'

    for part in robotroot.findall('part'):
        # print part.tag, part.attrib
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print 'processing part = ' + part.get('name')
            for brd in part.findall('board'):
                prp = get_board_properties(boardroot, brd.get('type'))

                if ('all' == targetboard) or (targetboard == brd.get('type')):

                    countOfFound = countOfFound + 1
                    details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)

                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print '- EXCLUSION #' + str(countOfExcluded)
                            print '  - of: ' + details

                    else:
    
                        countOfAttempts = countOfAttempts + 1

                        estimatedTimeForFWupdate = estimatedTimeForFWupdate + getTimeOfFirmwareUpdate(brd.get('type'))

                        if _verbose > 0:
                            print '- OPERATION #' + str(countOfAttempts)
                            print '  - type: info from xml file'
                            print '  - target: ' + details

                        r = print_board_info(part.get('name'), brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)'
                            # exit()
                        elif _verbose > 0:
                            print '  - result: SUCCESS'

                    # end of: if _excl...  

                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part


    if _verbose > 0:
        print_result('info()', countOfFound, countOfExcluded, countOfFailures)
        mi = estimatedTimeForFWupdate // 60
        ho = mi // 60
        h = ho
        m = mi % 60
        s = estimatedTimeForFWupdate % 60
        print '-- Estimated time for fw update: ' + str(estimatedTimeForFWupdate) + ' seconds (' + str(h) + 'h' + str(m) + 'm' + str(s) + 's)'
        print '--'
    # end of if ...

    return r

# end of: def info()

def print_result(nameOfCaller, nFound, nExcluded, nFailures):

    print '--'
    print '-- FINAL REPORT for ' + str(nameOfCaller) 
    print '-- Number of boards matching your criteria (w/ --part ' + _part + ' --board ' + _board + '): ' + str(nFound) 
    print '-- Number of boards excluded from the above number (w/ --excludeboard ' + _excludedboard + '): ' + str(nExcluded)
    print '-- Number of boards for which the operation was attempted: ' + str(nFound - nExcluded)
    print '-- Number of boards for which the operation had success: ' + str(nFound - nExcluded - nFailures)
    print '-- Number of boards for which the operation failed: ' + str(nFailures)  
    print '--'

# end of: def print_result()


# main entrance
if __name__ == '__main__':

    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='This script is a front-end for the FirmwareUpdater program in non GUI mode. ' +
                                                 'It performs automatic firmware update on the whole robot, on parts of it, or even on selected board types. ' +
                                                 'It exploits two xml files: the first is proper of the robot and contains its topology (which boards, on which driver and address), ' +
                                                 'whereas the second is common to all robots and contains the properties and location of the .hex files.' +
                                                 '\n' + 'Typical usage is:' + '\n' + 'python updateRobot.py -t topology.iCubGenova02.xml -f firmware.info.xml', formatter_class=RawTextHelpFormatter)

    parser.add_argument("-v", "--verbosity", type=int, action="store", required=False, default=1, choices=[0, 1, 2, 3], 
                    help="enables output verbosity. The printed output is: if 0 none, if 1 only basic python output, if every python output, if 2 also FirmwareUpdater. default = 0")
    parser.add_argument('-t', '--topology', action='store', required=True, type=argparse.FileType('r'),
                    help='the .xml file with the description of the robot in parts and boards')
    parser.add_argument('-f', '--firmware', action='store', required=True, type=argparse.FileType('r'),
                    help='the .xml file with the properties of the firmware of the boards (file path, fw version, etc.)')
    parser.add_argument('-p', '--part', action='store', required=False, default='all',
                    choices=['all', 'head', 'face', 'left_arm', 'right_arm', 'torso', 'left_leg', 'right_leg', 'custom', 'test'],
                    help='the part on which to perform the action. default = all')
    parser.add_argument('-b', '--board', action='store', required=False, default='all', 
                    choices=['all', 'ems4', 'mc4plus', 'mc2plus', 'mtb', 'mtb4', 'strain', 'strain2', 'foc', 'mc4', 'mais', 'bll', 'dsp'],
                    help='the board on which to perform the action. default = all')
    parser.add_argument('-xb', '--excludeboard', action='store', required=False, default='none', 
                    choices=['none', 'ems4', 'mc4plus', 'mc2plus', 'mtb', 'mtb4', 'strain', 'strain2', 'foc', 'mc4', 'mais', 'bll', 'dsp'],
                    help='exclude a board on which to perform the action. default = none')
    parser.add_argument('-a', '--action', action='store', required=True, default='info', choices=['info', 'update', 'forcemaintenance', 'forceapplication'],
                    help='the action to perform on on board(s) selected by --part and --board.')
    parser.add_argument("-d", "--debug", action="store_true", default=0,
                    help="enables debug mode. its use is reserved to developers and is hence undocumented. default = 0")


    args = parser.parse_args()  

    # pass parameters to program

    _verbosity = args.verbosity
    _filerobot = args.topology.name
    _fileboards = args.firmware.name
    _part = args.part
    _board = args.board
    _action = args.action
    _debugmode = args.debug
    _excludedboard = args.excludeboard



    # some warnings ...

    if _debugmode:
        print 'warning: debugmode is enabled!'

    if 0 == _verbosity:
        _verbose = 0 
        _verbosityFU = 0
    elif 1 == _verbosity:
        print "verbosity turned on for basic python only" 
        _verbose = 1 
        _verbosityFU = 0
    elif 2 == _verbosity:
        print "verbosity turned on for full python only" 
        _verbose = 2 
        _verbosityFU = 0
    else: 
        print "verbosity turned on for full python and FirmwareUpdater" 
        _verbose = 3 
        _verbosityFU = 1





    # open the xml files: one for robot description and one for board properties
    
    import xml.etree.ElementTree as ET
    xmltreeOfRobot = ET.parse(_filerobot)
    xmlrootOfRobot = xmltreeOfRobot.getroot()
    xmltreeOfBoards = ET.parse(_fileboards)
    xmlrootOfBoards = xmltreeOfBoards.getroot()



    # so far so good: now execute the action

    if _action == 'info':
        r = info(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'update':
        r = update(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'forcemaintenance':
        r = maintenance(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'forceapplication':
        r = application(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    else:
        print 'unsupported action: ' + _action


