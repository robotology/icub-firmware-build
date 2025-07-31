#!/usr/bin/env python3


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
# this script is a front-end for the FirmwareUpdater program in non GUI mode. it performs automatic firmware programs on robots.

import os
import sys

pyprefix = 'PY: '
debugprefix = '    [debug] '
errorprefix = '    [error] '

# it retrieves properties of a given board
def get_board_properties(boardroot, brdtype):
    prop = {}

    for p in boardroot.findall('board'):
        if brdtype == p.get('type'):
            prop = p
    return prop
# end of: def


def get_string_of_fulldescriptionofboard(brd):

    sss = 'board = ' + brd.get('type') + ', name = ' + brd.get('name')

    if None != brd.find('version'):
        if brd.get('required', '') == 'version':
            version = ', required firmware version = '
        else:
            version = ', firmware version = '
        targetversion = brd.find('version').attrib
        tmajor = targetversion.get('major', '0')
        tminor = targetversion.get('minor', '0')
        tbuild = targetversion.get('build', '0')
        sss = sss + version + tmajor + '.' + tminor + '.' + tbuild

    sss = sss + ', device = ' + brd.find('ondevice').text + ', address = ' + from_board_to_stringofaddress(brd)
    return sss
# end of: def

def eval_equal_or_zero(target, value):
    if target == '0':
        return True
    elif target == value:
        return True
    else:
        return False
# end of: def

# it retrieves properties of a given board
def get_board_properties2(boardroot, brd):
    prop = {}

    targetbrdtype = brd.get('type')
    findAlsoByVersion = False
    major = 0
    minor = 0
    build = 0
    if brd.get('required', '') == 'version':
        findAlsoByVersion = True       
        if None == brd.find('version'):
            print (pyprefix + errorprefix + 'syntax error in the xml robot network: cannot find tag <version> as indicated by <board type= .... required="version">'  )
            print (pyprefix + errorprefix + 'i will not consider this board. please rewrite the xml file.')
            return prop
        targetversion = brd.find('version').attrib
        tmajor = targetversion.get('major', '0')
        tminor = targetversion.get('minor', '0')
        tbuild = targetversion.get('build', '0')
    elif brd.get('required', '') != '':
        print (pyprefix + errorprefix + 'syntax error in the xml robot network: <board type= .... required="' + brd.get('required') +'"> is not allowed. if required is present, it can be only: ="version"')
        print (pyprefix + errorprefix + 'i will not consider this board. please rewrite the xml file.')
        return prop

    for p in boardroot.findall('board'):
        if targetbrdtype == p.get('type'):
            if findAlsoByVersion == False:
                prop = p
                break
            else:
                # must match also the major.mino.build etc.
                fw = p.find('firmware')
                ma = fw.find('version').get('major', '0')
                mi = fw.find('version').get('minor', '0')
                bu = fw.find('version').get('build', '0')
                if (True == eval_equal_or_zero(tmajor, ma)) and (True == eval_equal_or_zero(tminor, mi)) and (True == eval_equal_or_zero(tbuild, bu)):
                    prop = p
                    break 
        
    return prop
# end of: def


# it retrieves the address of a board in string form
def from_board_to_stringofaddress(brd):
    adr = brd.find('ataddress').attrib
    ss = adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')
    return ss
# end of: def

# it retrieves the ip address of a board in string form
def from_board_to_stringofIPaddress(brd):
    adr = brd.find('ataddress').attrib
    ss = adr.get('ip', '0')
    return ss
# end of: def

# it retrieves the address of a board in string form
def from_board_to_stringofrequiredversion(brd):
    sss = ''
    if brd.get('required') != 'version':
        return sss
    ver = brd.find('version').attrib
    sss = ver.get('major', '0') + '.' + ver.get('minor', '0') + '.' + ver.get('build', '0')
    return sss
# end of: def

# it retrieves the firmware version of a board in string form
def from_firmware_to_stringofversion(fw):
    ss = fw.find('version').get('major', '0') + '.' + fw.find('version').get('minor', '0') + '.' + fw.find('version').get('build', '0')
    return ss
# end of: def


# it retrieves the firmware version of a board in string form for ETH boards
def from_firmware_to_stringofversionETH(fw):
    ss = fw.find('version').get('major', '0') + '.' + fw.find('version').get('minor', '0')
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
        print (pyprefix + debugprefix + 'eth_force_maintenance(): sending eth board in maintenance mode w/ command:')
        print (pyprefix + debugprefix+ command)

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 != r:
        print (pyprefix + errorprefix + 'eth_force_maintenance(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip'))
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
        print (pyprefix + debugprefix + 'eth_force_application(): sending eth board in application mode w/ command:')
        print (pyprefix + debugprefix + command)

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)
    
    r = r / 256

    if 0 != r:
        print (pyprefix + errorprefix + 'eth_force_application(): FAILURE sending in application mode eth board @ ' + adr.get('ip'))
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
            print (pyprefix + errorprefix + 'goto_maintenance(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported')
            r = 1        
    elif 'CFW' == ondevice:
        print (pyprefix + '    [info]: boards on device ' + ondevice + ' dont need to be forced in maintenance mode!'   )
        r = 0
    else:
        print (pyprefix + errorprefix + 'goto_maintenance(): FAILURE the device ' + ondevice + ' is unsupported')
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
            print (pyprefix + errorprefix + 'goto_application(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported')
            r = 1        
    elif 'CFW' == ondevice:
        print (pyprefix + '    [info]: boards on device ' + ondevice + ' dont need to be forced in application mode!'  )
        r = 0  
    else:
        print (pyprefix + errorprefix + 'goto_application(): FAILURE the device ' + ondevice + ' is unsupported')
        r = 1

    return r
# end of: def

# it performs fw verify of cfw device 
def do_firmware_verify_cfw(brd, prp):
    r = 2
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_cfw(): performing fw verify on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

    stringOfCANfwversion = from_firmware_to_stringofversion(fw)
    tmp1 = 'FirmwareUpdater --nogui --verify ' + stringOfCANfwversion + ' --device CFW2 --id ' +  adr.get('canbus', '0')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_cfw(): verifying can firmware w/ command:')
        print (pyprefix + debugprefix + command )

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 == r:
        r = 0
    elif 1 == r:
        if _verbose > 1:
            print (pyprefix + debugprefix + 'do_firmware_verify_cfw(): TODO update FW of can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
        return r 
    else:
        print (pyprefix + errorprefix + 'do_firmware_verify_cfw(): ERROR cannot find can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
        return r     

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_cfw(): FW is OK!')

    return r
# end of: def



# it performs fw verify of can over eth device
def do_firmware_verify_canovereth(brd, prp):
    r = 2
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_canovereth(): performing fw verify on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

    r = eth_force_maintenance(brd, prp)

    if 0 != r:
        print (pyprefix + errorprefix + 'do_firmware_verify_canovereth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip', '0'))
        return r   

    stringOfCANfwversion = from_firmware_to_stringofversion(fw)
    tmp1 = 'FirmwareUpdater --nogui --verify ' + stringOfCANfwversion + ' --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_canovereth(): verifying can firmware w/ command:')
        print (pyprefix + debugprefix + command )


    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 == r:
        r = 0
    elif 1 == r:
        if _verbose > 1:
            print (pyprefix + debugprefix + 'do_firmware_verify_canovereth(): TODO update FW of can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
        return r 
    else:
        print (pyprefix + errorprefix + 'do_firmware_verify_canovereth(): ERROR cannot find can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
        return r 

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_canovereth(): FW is OK!')

    return r
# end of: def


# it performs firmware verify by calling the external program
def do_firmware_verify_eth(brd, prp):
    r = 2
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_eth(): performing fw verify on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

#    r = eth_force_maintenance(brd, prp)
#
#    if 0 != r:
#        print (pyprefix + errorprefix + 'do_firmware_verify_eth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip', '0'))
#        return r     

    stringOfETHfwversion = from_firmware_to_stringofversionETH(fw)
    command = 'FirmwareUpdater --nogui --verify ' + stringOfETHfwversion + ' --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip', '0') + ' --verbosity ' + str(_verbosityFU)

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_eth(): verifying eth firmware w/ command:'        )
        print (pyprefix + debugprefix + command )

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 == r:
        r = 0
    elif 1 == r:
        if _verbose > 1:
            print (pyprefix + debugprefix + 'do_firmware_verify_eth(): TODO update FW of eth board @ ' + adr.get('ip', '0'))
        return r 
    else:
        print (pyprefix + errorprefix + 'do_firmware_verify_eth(): ERROR cannot find eth board @ ' + adr.get('ip', '0'))
        return r 

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_verify_eth(): FW is the latest one!')

    return r
# end of: def


# it selects what kind of fw verify to do: eth, eth:can, cfw
def do_firmware_verify(brd, prp):
    r = 2
    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = do_firmware_verify_eth(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = do_firmware_verify_canovereth(brd, prp)
        else:
            print (pyprefix + errorprefix + 'do_firmware_verify(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported')
            r = 2        
    elif 'CFW' == ondevice:
        r = do_firmware_verify_cfw(brd, prp)
    else:
        print (pyprefix + errorprefix + 'do_firmware_verify(): FAILURE the device ' + ondevice + ' is unsupported')
        r = 2

    return r
# end of: def


# it performs fw query of cfw device 
def do_firmware_query_cfw(brd, prp):
    r = 2
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_cfw(): performing query on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

    stringOfCANfwversion = from_firmware_to_stringofversion(fw)
    tmp1 = 'FirmwareUpdater --nogui --query' + ' --device CFW2 --id ' +  adr.get('canbus', '0')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_cfw(): querying can board type + firmware w/ command:')
        print (pyprefix + debugprefix + command )

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 == r:
        r = 0
    else:
         print (pyprefix + errorprefix + 'do_firmware_query_cfw(): ERROR cannot find can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
         return r     

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_cfw(): board is found!')

    return r
# end of: def



# it performs fw query of can over eth device
def do_firmware_query_canovereth(brd, prp):
    r = 2
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_canovereth(): performing query on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

    r = eth_force_maintenance(brd, prp)

    if 0 != r:
        print (pyprefix + errorprefix + 'do_firmware_query_canovereth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip', '0'))
        return r   

    #stringOfCANfwversion = from_firmware_to_stringofversion(fw)
    tmp1 = 'FirmwareUpdater --nogui --query' + ' --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_canovereth(): querying can board + firmware w/ command:')
        print (pyprefix + debugprefix + command )


    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 == r:
        r = 0
    else:
         print (pyprefix + errorprefix + 'do_firmware_query_canovereth(): ERROR cannot find can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
         return r 

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_canovereth(): FW is OK!')

    return r
# end of: def


# it performs firmware query by calling the external program
def do_firmware_query_eth(brd, prp):
    r = 2
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_eth(): performing fw query on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

#    r = eth_force_maintenance(brd, prp)
#
#    if 0 != r:
#        print (pyprefix + errorprefix + 'do_firmware_query_eth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip', '0'))
#        return r     

#    stringOfETHfwversion = from_firmware_to_stringofversionETH(fw)
    command = 'FirmwareUpdater --nogui --query' + ' --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip', '0') + ' --verbosity ' + str(_verbosityFU)

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_eth(): querying eth board + firmware w/ command:'        )
        print (pyprefix + debugprefix + command )

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 == r:
        r = 0
    else:
         print (pyprefix + errorprefix + 'do_firmware_query_eth(): ERROR cannot find eth board @ ' + adr.get('ip', '0'))
         return r 

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_query_eth(): board found!')

    return r
# end of: def


# it selects what kind of fw query to do: eth, eth:can, cfw
def do_firmware_query(brd, prp):
    r = 2
    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = do_firmware_query_eth(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = do_firmware_query_canovereth(brd, prp)
        else:
            print (pyprefix + errorprefix + 'do_firmware_query(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported')
            r = 2        
    elif 'CFW' == ondevice:
        r = do_firmware_query_cfw(brd, prp)
    else:
        print (pyprefix + errorprefix + 'do_firmware_query(): FAILURE the device ' + ondevice + ' is unsupported')
        r = 2

    return r
# end of: def



# it tells how long it takes to perform fw program
def getTimeOfFirmwareUpdate(brdtype):
    r = 666

    if brdtype == 'ems4':
        r = 15
    elif brdtype == 'mc4plus':
        r = 15
    elif brdtype == 'mc2plus':
        r = 15
    elif brdtype == 'foc':
        r = 105
    elif brdtype == 'foc-special':
        r = 105
    elif brdtype == 'mtb':
        r = 105
    elif brdtype == 'mtb4':
        r = 280
    elif brdtype == 'mtb4c':
        r = 280
    elif brdtype == 'mais':
        r = 50
    elif brdtype == 'strain':
        r = 70
    elif brdtype == 'strain2':
        r = 280
    elif brdtype == 'strain2c':
        r = 280
    elif brdtype == 'rfe':
        r = 280
    elif brdtype == 'mc4':
        r = 66
    elif brdtype == 'bll':
        r = 66
    elif brdtype == 'dsp':
        r = 66
    elif brdtype == 'amc':
        r = 30
    elif brdtype == 'amc2c':
        r = 30
    elif brdtype == 'amcbldc':
        r = 280
    else:
        r = 666

    return r
# end of: def




# it selects what kind of fw program to do: eth, eth:can, cfw
def do_firmware_program(brd, prp):
    r = 1
    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = do_firmware_program_eth(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = do_firmware_program_canovereth(brd, prp)
        else:
            print (pyprefix + errorprefix + 'do_firmware_program(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported')
            r = 1        
    elif 'CFW' == ondevice:
        r = do_firmware_program_cfw(brd, prp)
    else:
        print (pyprefix + errorprefix + 'do_firmware_program(): FAILURE the device ' + ondevice + ' is unsupported')
        r = 1

    return r
# end of: def

# it performs fw program of cfw device 
def do_firmware_program_cfw(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_cfw(): performing fw program on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))


    tmp1 = 'FirmwareUpdater --nogui --program --device CFW2 --id ' +  adr.get('canbus', '0')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --file ' + fw.find('file').text + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_cfw(): uploading can firmware w/ command:')
        print (pyprefix + debugprefix + command )

    if _verbose > 0:
        boardtype = brd.get('type')
        timeofupload = getTimeOfFirmwareUpdate(boardtype)
        print (pyprefix + '  - message: please be prepared to wait for some time ... fw program of a ' + boardtype + ' typically lasts ' + str(timeofupload) + ' seconds')

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 != r:
         print (pyprefix + errorprefix + 'do_firmware_program_cfw(): FAILURE programming can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
         return r 


    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_cfw(): done!')

    return r
# end of: def



# it performs fw program of can over eth device
def do_firmware_program_canovereth(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    
    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_canovereth(): performing fw program on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

    r = eth_force_maintenance(brd, prp)

    if 0 != r:
        print (pyprefix + errorprefix + 'do_firmware_program_canovereth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip', '0'))
        return r   

    tmp1 = 'FirmwareUpdater --nogui --program --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip', '0')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --file ' + fw.find('file').text + ' --verbosity ' + str(_verbosityFU)
    command = tmp1 + tmp2

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_canovereth(): uploading can firmware w/ command:')
        print (pyprefix + debugprefix + command )

    if _verbose > 0:
        boardtype = brd.get('type')
        timeofupload = getTimeOfFirmwareUpdate(boardtype)
        print (pyprefix + '  - message: please be prepared to wait for some time ... fw program of a ' + boardtype + ' typically lasts ' + str(timeofupload) + ' seconds')

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 != r:
         print (pyprefix + errorprefix + 'do_firmware_program_canovereth(): FAILURE programming can board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))
         return r 


    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_canovereth(): done!')

    return r
# end of: def


# it performs firmware program by calling the external program
def do_firmware_program_eth(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_eth(): performing fw program on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0'))

    r = eth_force_maintenance(brd, prp)

    if 0 != r:
        print (pyprefix + errorprefix + 'do_firmware_program_eth(): FAILURE sending in maintenance mode eth board @ ' + adr.get('ip', '0'))
        return r     

   
    command = 'FirmwareUpdater --nogui --program --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip', '0') + ' --file ' + fw.find('file').text + ' --verbosity ' + str(_verbosityFU)

    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_eth(): uploading eth firmware w/ command:'        )
        print (pyprefix + debugprefix + command )

    if _verbose > 0:
        boardtype = brd.get('type')
        timeofupload = getTimeOfFirmwareUpdate(boardtype)
        print (pyprefix + '  - message: please be prepared to wait for some time ... fw program of a ' + boardtype + ' typically lasts ' + str(timeofupload) + ' seconds')

    if 1 == _debugmode:
        r = 0
    else:
        r = os.system(command)

    r = r / 256

    if 0 != r:
         print (pyprefix + errorprefix + 'do_firmware_program_eth(): FAILURE programming eth board @ ' + adr.get('ip', '0'))
         return r 


    if _verbose > 1:
        print (pyprefix + debugprefix + 'do_firmware_program_eth(): done!')

    return r
# end of: def


#print (pyprefix + 'processing: part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd))

def get_string_of_firmwareproperties(prp):
    fw = prp.find('firmware')
    sss = 'required firmware version = ' + from_firmware_to_stringofversion(fw) + ', file location = ' + fw.find('file').text
    return sss
# end of: def

# it prints info about a given board as found in firmware xml file
def print_firmware_info(partname, brd, prp):
    r = 0
    print (pyprefix + '  - [INFO]  board = ' + brd.get('type') + ', ' + get_string_of_firmwareproperties(prp))
    import os.path
    fw = prp.find('firmware')
    fname = fw.find('file').text
    if False == os.path.exists(fname):
        print (pyprefix + '  - [ERROR] file ' + fname + ' does not exist')
        return 1                  
    return r
# end of: def


# 0 is ok programmed, 1 is ko programming, 10 is no need to program
# it selects what kind of fw update to do: eth, eth:can, cfw
def do_firmware_update(brd, prp):
    r = 1
    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:

        if 0 == adr.get('canbus', 0):

            r = do_firmware_verify_eth(brd, prp)

            if 0 == r:
                print (pyprefix + '  - message: the board already has the most recent FW.')
                r = 10
                if _verbose > 1:
                    adr = brd.find('ataddress').attrib
                    print (pyprefix + debugprefix + 'do_firmware_update(): no need to program board @ ' + adr.get('ip', '0')    )
            elif 1 == r:
                print (pyprefix + '  - message: the board has an old FW which is going to be updated.')
                if _verbose > 1:
                    print (pyprefix + debugprefix + 'do_firmware_update(): will program board @ ' + adr.get('ip', '0'))
                r = do_firmware_program_eth(brd, prp)
            else:
                print (pyprefix + errorprefix + 'do_firmware_update(): FAILURE because cannot verify board @ ' + adr.get('ip', '0') )

        elif 0 != adr.get('canadr', 0):

            r = do_firmware_verify_canovereth(brd, prp)

            if 0 == r:
                print (pyprefix + '  - message: the board already has the most recent FW.')
                r = 10
                if _verbose > 1:
                    adr = brd.find('ataddress').attrib
                    print (pyprefix + debugprefix + 'do_firmware_update(): no need to program board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')    )
            elif 1 == r:
                print (pyprefix + '  - message: the board has an old FW which is going to be updated.')
                if _verbose > 1:
                    print (pyprefix + debugprefix + 'do_firmware_update(): will program board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') )
                r = do_firmware_program_canovereth(brd, prp)
            else:
                print (pyprefix + errorprefix + 'do_firmware_update(): FAILURE because cannot find board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') )

        else:

            print (pyprefix + errorprefix + 'do_firmware_update(): FAILURE the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported')
            r = 2   
     
    elif 'CFW' == ondevice:

        r = do_firmware_verify_cfw(brd, prp)

        if 0 == r:
            print (pyprefix + '  - message: the board already has the most recent FW.')
            r = 10
            if _verbose > 1:
                adr = brd.find('ataddress').attrib
                print (pyprefix + debugprefix + 'do_firmware_update(): no need to program board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')    )
        elif 1 == r:
            print (pyprefix + '  - message: the board has an old FW which is going to be updated.')
            if _verbose > 1:
                print (pyprefix + debugprefix + 'do_firmware_update(): will program board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') )
            r = do_firmware_program_cfw(brd, prp)
        else:
            print (pyprefix + errorprefix + 'do_firmware_update(): FAILURE because cannot find board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') )

    else:
        print (pyprefix + errorprefix + 'do_firmware_update(): FAILURE the device ' + ondevice + ' is unsupported')
        r = 1

    return r
# end of: def




# query fw versions of all the boards in the xml file which are inside targetpart and are targetboard
def query(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --query request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                
                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: firmware query')
                            print (pyprefix + '  - target: ' + details)
                            print (pyprefix + '  - using:  ' + get_string_of_firmwareproperties(prp))

                        r = do_firmware_query(brd, prp)


                        if 0 == r:
                            if _verbose > 0:
                                print (pyprefix + '  - result: SUCCESS!! found the board')
                        elif 1 == r:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! the remote board cannot be found')
                        else:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! unknown return value from FirmwareUpdater =' + r)

                    # end of: if _excl...
                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    if _verbose > 0:
        print_result('verify()', countOfFound, countOfExcluded, countOfFailures)
    # end of if ...

    return 
# end of: def verify



# verify fw versions of all the boards in the xml file which are inside targetpart and are targetboard
def verify(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0
    countOfRequiredUpdates = 0

    estimatedTimeForFWprogram = 0

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --verify request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                
                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: firmware verify')
                            print (pyprefix + '  - target: ' + details)
                            print (pyprefix + '  - using:  ' + get_string_of_firmwareproperties(prp))

                        r = do_firmware_verify(brd, prp)


                        if 0 == r:
                            if _verbose > 0:
                                print (pyprefix + '  - result: SUCCESS!! the fw version on remote board matches the requirements')
                        elif 1 == r:
                            countOfRequiredUpdates = countOfRequiredUpdates + 1
                            brdtime = getTimeOfFirmwareUpdate(brd.get('type'))
                            estimatedTimeForFWprogram = estimatedTimeForFWprogram + brdtime
                            print (pyprefix + '  - result: ACTION!! the fw version of remote board must be updated (estimated time = ' + str(brdtime) + ' seconds)')
                        elif 2 == r:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! the remote board cannot be found')
                        else:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! unknown return value from FirmwareUpdater =' + r)

                    # end of: if _excl...
                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    if _verbose > 0:
        print_result('verify()', countOfFound, countOfExcluded, countOfFailures)
        print (pyprefix + '-- Number of boards which need FW update: ' + str(countOfRequiredUpdates))
        mi = estimatedTimeForFWprogram // 60
        ho = mi // 60
        h = ho
        m = mi % 60
        s = estimatedTimeForFWprogram % 60
        print (pyprefix + '-- Estimated time for FW program of boards w/ old FW version: ' + str(estimatedTimeForFWprogram) + ' seconds (' + str(h) + 'h' + str(m) + 'm' + str(s) + 's)')
        print (pyprefix + '--')
    # end of if ...
    # end of if ...

    return 
# end of: def verify


# send in maintenance all the boards in the xml file which are inside targetpart and are targetboard
def maintenance(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --forcemaintenance request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                    
                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):

                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: force maintenance')
                            print (pyprefix + '  - target: ' + details                  )
                        
                        r = goto_maintenance(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)')
                            # exit()
                        elif _verbose > 0:
                            print (pyprefix + '  - result: SUCCESS')

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



# program all the boards in the xml file which are inside targetpart and are targetboard
def program(targetpart, targetboard, robotroot, boardroot, verbose):
    # Check for parallel argument from main
    import inspect
    import subprocess
    frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(frame)
    caller_locals = outer_frames[1].frame.f_locals
    parallel = caller_locals.get('_parallel', False)

    if parallel:
        from collections import defaultdict
        eth_can_groups = defaultdict(lambda: defaultdict(list))  # {eth_ip: {firmware_file: [CANx:y, ...]}}
        eth_boards_to_program = []
        found_any_board = False

        for part in robotroot.findall('part'):
            if ('all' == targetpart) or (targetpart == part.get('name')):
                for brd in part.findall('board'):
                    found_any_board = True
                    prp = get_board_properties2(boardroot, brd)
                    if len(prp) == 0:
                        continue
                    if ('all' == targetboard) or (targetboard == brd.get('type')):
                        if _excludedboard == brd.get('type'):
                            continue
                        if brd.find('ondevice').text == 'ETH':
                            adr = brd.find('ataddress').attrib
                            ip = adr.get('ip', None)
                            canbus = adr.get('canbus', None)
                            canadr = adr.get('canadr', None)
                            if ip and canbus and canadr:
                                firmware_file = prp.find('firmware').find('file').text
                                can_addr = f'CAN{canbus}:{canadr}'
                                eth_can_groups[ip][firmware_file].append(can_addr)
                            elif ip and (canbus is None or canbus == '0') and (canadr is None or canadr == '0'):
                                # ETH-only board (main ETH board)
                                eth_boards_to_program.append((brd, prp))  # <-- ADD THIS LINE

        if not found_any_board:
            print(pyprefix + f'[parallel][WARNING] No boards found in network XML for part="{targetpart}" and board="{targetboard}".')
            return
        
        # 1. Program all CAN-over-ETH boards in parallel (grouped by ETH IP and firmware file)
        for ipaddress, fw_groups in eth_can_groups.items():
            # Ensure ETH board is in maintenance mode
            eth_brd = None
            for part in robotroot.findall('part'):
                for brd in part.findall('board'):
                    if brd.find('ondevice').text == 'ETH':
                        adr = brd.find('ataddress').attrib
                        if adr.get('ip', None) == ipaddress and not ('canbus' in adr and adr['canbus'] != '0'):
                            eth_brd = brd
                            break
                if eth_brd:
                    break
            if not eth_brd:
                print(pyprefix + f'[parallel] ERROR: Could not find ETH board {ipaddress} in XML.')
                continue
            prp = get_board_properties2(boardroot, eth_brd)
            r_maint = eth_force_maintenance(eth_brd, prp)
            if r_maint != 0:
                print(pyprefix + f'[parallel] ERROR: Failed to put ETH board {ipaddress} in maintenance mode.')
                continue

            for firmware_file, can_addresses in fw_groups.items():
                addresses_str = ' '.join(can_addresses)
                command = f'FirmwareUpdater --nogui --device ETH --id eth1 --eth_board {ipaddress} --addresses "{addresses_str}" --file {firmware_file} --program'
                print(f'FirmwareUpdater --nogui --device ETH --id eth1 --eth_board {ipaddress} --addresses "{addresses_str}" --file {firmware_file} --program')
                print(pyprefix + f'[parallel] Running: {command}')
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                board_results = {}
                for line in proc.stdout:
                    print(line, end='')  # Still print all output
                    if "All Board OK" in line:
                        for addr in can_addresses:
                            board_results[addr] = "SUCCESS"
                proc.wait()
                if proc.returncode == 0:
                    print(pyprefix + '[parallel] SUCCESS')
                else:
                    print(pyprefix + '[parallel] FAILURE')
                if board_results:
                    print(pyprefix + '[parallel] Board programming summary:')
                    for board, result in board_results.items():
                        print(f"{pyprefix}    {board}: {result}")

        # 2. Program all ETH-only boards sequentially (one by one)
        eth_success = []
        for brd, prp in eth_boards_to_program:
            prp = get_board_properties2(boardroot, brd)  # Always get the correct firmware info for this board
            print(pyprefix + f'[parallel] Programming ETH board {from_board_to_stringofaddress(brd)} using do_firmware_program_eth()')
            r = do_firmware_program_eth(brd, prp)
            adr = brd.find('ataddress').attrib
            ip = adr.get('ip', None)
            if r == 0:
                print(pyprefix + f'[parallel][ETH {ip}] SUCCESS')
                eth_success.append(ip)
            else:
                print(pyprefix + f'[parallel][ETH {ip}] FAILURE')

        if eth_success:
            print(pyprefix + '[parallel] ETH boards successfully programmed:')
            for ip in eth_success:
                print(pyprefix + f'    ETH {ip}')
        return

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --program request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                
                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: firmware program')
                            print (pyprefix + '  - target: ' + details)
                            print (pyprefix + '  - using:  ' + get_string_of_firmwareproperties(prp))

                        r = do_firmware_program(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)')
                            # exit()
                        elif _verbose > 0:
                            print (pyprefix + '  - result: SUCCESS')

                    # end of: if _excl...
                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    if _verbose > 0:
        print_result('program()', countOfFound, countOfExcluded, countOfFailures)
    # end of if ...

    return 
# end of: def program


# update all the boards in the xml file which are inside targetpart and are targetboard
def update(targetpart, targetboard, robotroot, boardroot, verbose):
    import inspect
    import subprocess
    frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(frame)
    caller_locals = outer_frames[1].frame.f_locals
    parallel = caller_locals.get('_parallel', False)

    # For parallel update
    eth_boards = []
    can_addresses = []
    firmware_file = None
    found_any_board = False
    found_any_eth = False
    all_can_boards = []

    # First pass: collect ETH:CAN boards that need update
    if parallel:
        from collections import defaultdict
        eth_can_groups = defaultdict(lambda: defaultdict(list))  # {eth_ip: {firmware_file: [CANx:y, ...]}}
        found_any_board = False

        for part in robotroot.findall('part'):
            if ('all' == targetpart) or (targetpart == part.get('name')):
                for brd in part.findall('board'):
                    prp = get_board_properties2(boardroot, brd)
                    if len(prp) == 0:
                        continue
                    if ('all' == targetboard) or (targetboard == brd.get('type')):
                        if _excludedboard == brd.get('type'):
                            continue
                        if brd.find('ondevice').text == 'ETH':
                            adr = brd.find('ataddress').attrib
                            ip = adr.get('ip', None)
                            canbus = adr.get('canbus', None)
                            canadr = adr.get('canadr', None)
                            # Only CAN boards (not ETH main board)
                            if ip and canbus and canadr and canadr != '0':
                                # Only add if firmware is old (needs update)
                                r = do_firmware_verify_canovereth(brd, prp)
                                if r == 1:
                                    firmware_file = prp.find('firmware').find('file').text
                                    can_addr = f'CAN{canbus}:{canadr}'
                                    eth_can_groups[ip][firmware_file].append(can_addr)
                                    found_any_board = True

        if not found_any_board:
            print(pyprefix + f'[parallel][WARNING] No CAN boards needing update found in network XML for part="{targetpart}" and board="{targetboard}".')
            return

        for ipaddress, fw_groups in eth_can_groups.items():
            # Ensure ETH board is in maintenance mode
            eth_brd = None
            for part in robotroot.findall('part'):
                for brd in part.findall('board'):
                    if brd.find('ondevice').text == 'ETH':
                        adr = brd.find('ataddress').attrib
                        if adr.get('ip', None) == ipaddress and not ('canbus' in adr and adr['canbus'] != '0'):
                            eth_brd = brd
                            break
                if eth_brd:
                    break
            if not eth_brd:
                print(pyprefix + f'[parallel] ERROR: Could not find ETH board {ipaddress} in XML.')
                continue
            prp = get_board_properties2(boardroot, eth_brd)
            r_maint = eth_force_maintenance(eth_brd, prp)
            if r_maint != 0:
                print(pyprefix + f'[parallel] ERROR: Failed to put ETH board {ipaddress} in maintenance mode.')
                continue

            for firmware_file, can_addresses in fw_groups.items():
                addresses_str = ' '.join(can_addresses)
                command = f'FirmwareUpdater --nogui --device ETH --id eth1 --eth_board {ipaddress} --addresses "{addresses_str}" --file {firmware_file} --program'
                print(f'FirmwareUpdater --nogui --device ETH --id eth1 --eth_board {ipaddress} --addresses "{addresses_str}" --file {firmware_file} --program')
                print(pyprefix + f'[parallel] Running: {command}')
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                board_results = {}
                for line in proc.stdout:
                    print(line, end='')  # Still print all output
                    if "All Board OK" in line:
                        for addr in can_addresses:
                            board_results[addr] = "SUCCESS"
                proc.wait()
                if proc.returncode == 0:
                    print(pyprefix + '[parallel] SUCCESS')
                else:
                    print(pyprefix + '[parallel] FAILURE')
                if board_results:
                    print(pyprefix + '[parallel] Board programming summary:')
                    for board, result in board_results.items():
                        print(f"{pyprefix}    {board}: {result}")
        return

    # Normal (non-parallel) update logic
    r = 1
    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --update request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                
                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: firmware update')
                            print (pyprefix + '  - target: ' + details)
                            print (pyprefix + '  - using:  ' + get_string_of_firmwareproperties(prp))

                        r = do_firmware_update(brd, prp)

                        if 0 == r:
                            if _verbose > 0:
                                print (pyprefix + '  - result: SUCCESS: the board has been programmed with latest firmware version')
                        elif 10 == r:
                            if _verbose > 0:
                                print (pyprefix + '  - result: SUCCESS: the board already has the latest version of firmware')
                        else:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)')
                            # exit()


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
        print (pyprefix + '[debug] processing a --forcemaintenance request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):
                    
                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):

                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:

                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: force maintenance')
                            print (pyprefix + '  - target: ' + details                  )
                        
                        r = goto_maintenance(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)')
                            # exit()
                        elif _verbose > 0:
                            print (pyprefix + '  - result: SUCCESS')

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
        print (pyprefix + '[debug] processing a --forceapplication request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):

                    countOfFound = countOfFound + 1
                    # details = 'part = ' + part.get('name') + ', board = ' + brd.get('type') + ', name = ' + brd.get('name') + ', address = ' + from_board_to_stringofaddress(brd)
                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)

                    if _excludedboard == brd.get('type'):

                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:
                    
                        countOfAttempts = countOfAttempts + 1

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: force application')
                            print (pyprefix + '  - target: ' + details)
     
                        r = goto_application(brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                           
                            print (pyprefix + '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)')
                            # exit()
                        elif _verbose > 0:
                            print (pyprefix + '  - result: SUCCESS')

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

    estimatedTimeForFWprogram = 0;

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --info request:')

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)

                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):

                    countOfFound = countOfFound + 1

                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)
 
                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:
    
                        countOfAttempts = countOfAttempts + 1

                        estimatedTimeForFWprogram = estimatedTimeForFWprogram + getTimeOfFirmwareUpdate(brd.get('type'))

                        if _verbose > 0:
                            print (pyprefix + '- OPERATION #' + str(countOfAttempts))
                            print (pyprefix + '  - type: info from xml file')
                            print (pyprefix + '  - target: ' + details)

                        r = print_firmware_info(part.get('name'), brd, prp)

                        if 0 != r:
                            countOfFailures = countOfFailures + 1
                            print (pyprefix + '  - result: FAILURE!! (However, the operation will be attempted with other boards until completion)')
                            # exit()
                        elif _verbose > 0:
                            print (pyprefix + '  - result: SUCCESS')

                    # end of: if _excl...  

                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part


    if _verbose > 0:
        print_result('info()', countOfFound, countOfExcluded, countOfFailures)
        mi = estimatedTimeForFWprogram // 60
        ho = mi // 60
        h = ho
        m = mi % 60
        s = estimatedTimeForFWprogram % 60
        print (pyprefix + '-- Estimated time for FW program of all boards: ' + str(estimatedTimeForFWprogram) + ' seconds (' + str(h) + 'h' + str(m) + 'm' + str(s) + 's)')
        print (pyprefix + '--')
    # end of if ...

    return r

# end of: def info()


def findInprev(currIP, targetpart, targetboard, robotroot, boardroot, verbose):

    brd1 = 'none'

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    #print 'looking for a prev = ' + currIP

    for part in robotroot.findall('part'):
        # print (pyprefix + part.tag, part.attrib)
        if ('all' == targetpart) or (targetpart == part.get('name')):
            #print (pyprefix + 'processing part = ' + part.get('name'))
            for brd in part.findall('board'):

                prp = get_board_properties2(boardroot, brd)
                if len(prp) == 0:
                    print (pyprefix + errorprefix + 'cannot find a match for ' + 'following board' + ' in firmware xml file. i continue parsing other boards of network file')
                    print (pyprefix + errorprefix + 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd))
                    continue

                if ('all' == targetboard) or (targetboard == brd.get('type')):


                    details = 'part = ' + part.get('name') + ', ' + get_string_of_fulldescriptionofboard(brd)
 
                    if _excludedboard == brd.get('type'):
                        
                        countOfExcluded = countOfExcluded + 1
                        if _verbose > 0:
                            print (pyprefix + '- EXCLUSION #' + str(countOfExcluded))
                            print (pyprefix + '  - of: ' + details)

                    else:
    

                        if 'ETH' == brd.find('ondevice').text:

                            if None != brd.find('connected'):

                                con = brd.find('connected').attrib
                                ss = con.get('prev', '0')
                            
                                adr = from_board_to_stringofaddress(brd);
                                # print 'eval: ' + adr
                        
                                if ss == currIP:
                                    #print 'found:' + adr
                                    return brd


                    # end of: if _excl...  

                # end of: if targetboard
            # end of: for brd
        # end of: if targetpart
    # end of: for part

    return brd1

# end of: def findInprev()


# prints info on topology
def topology(targetpart, targetboard, robotroot, boardroot, verbose):

    r = 1

    countOfFound = 0
    countOfExcluded = 0
    countOfFailures = 0
    countOfAttempts = 0

    estimatedTimeForFWprogram = 0;

    if _verbose > 1:
        print (pyprefix + '[debug] processing a --topology request:')

    currIP = '10.0.1.104'
    nextIP = 'none'
    prevIP = 'none'

    print (pyprefix + '<ETH> (in daisy chain order)' )
    #print (pyprefix + '  | (in daisy chain order)')
    print (pyprefix + '   -> 10.0.1.104 [linux host] ->')

    while True:
        brd = findInprev(currIP, targetpart, targetboard, robotroot, boardroot, verbose)
        if 'none' == brd:
            break
        print (pyprefix + '   -> ' + from_board_to_stringofIPaddress(brd) + ' [' + brd.get('type') + ', ' + brd.get('name') + '] ->')
        adr = brd.find('ataddress').attrib
        currIP = adr.get('ip', '0')
    
    print (pyprefix + '   -> END')
    print (pyprefix + '</ETH>')


    return r
# end of: def topology()


def print_result(nameOfCaller, nFound, nExcluded, nFailures):

    print (pyprefix + '--')
    print (pyprefix + '-- FINAL REPORT for ' + str(nameOfCaller) )
    print (pyprefix + '-- Number of boards matching your criteria (w/ --part ' + _part + ' --board ' + _board + '): ' + str(nFound) )
    print (pyprefix + '-- Number of boards excluded from the above number (w/ --excludeboard ' + _excludedboard + '): ' + str(nExcluded))
    print (pyprefix + '-- Number of boards for which the operation was attempted: ' + str(nFound - nExcluded))
    print (pyprefix + '-- Number of boards for which the operation had success: ' + str(nFound - nExcluded - nFailures))
    print (pyprefix + '-- Number of boards for which the operation failed: ' + str(nFailures)   )
    print (pyprefix + '--')

# end of: def print_result()


# main entrance
if __name__ == '__main__':

    import argparse

    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='This script is a front-end for the FirmwareUpdater program in non GUI mode. ' +
                                                 'It performs automatic firmware program on the whole robot, on parts of it, or even on selected board types. ' +
                                                 'It exploits two xml files: the first is proper of the robot and contains its network (which boards, on which driver and address), ' +
                                                 'whereas the second is common to all robots and contains the properties and location of the .hex files.' +
                                                 '\n' + 'Typical usage is:' + '\n' + 'python manageFWrobot.py -t network.iCubGenova02.xml -f firmware.info.xml -a info', formatter_class=RawTextHelpFormatter)

    parser.add_argument("-v", "--verbosity", type=int, action="store", required=False, default=1, choices=[0, 1, 2, 3], 
                    help="enables output verbosity. The printed output is: if 0 none, if 1 only basic python output, if every python output, if 2 also FirmwareUpdater. default = 0")
    parser.add_argument('-n', '--network', action='store', required=True, type=argparse.FileType('r'),
                    help='the .xml file with the description of the robot in parts and boards')
    parser.add_argument('-f', '--firmware', action='store', required=True, type=argparse.FileType('r'),
                    help='the .xml file with the properties of the firmware of the boards (file path, fw version, etc.)')
    parser.add_argument('-p', '--part', action='store', required=False, default='all',
                    choices=['all', 'head', 'face', 'left_arm', 'right_arm', 'torso', 'left_leg', 'right_leg', 'custom', 'test'],
                    help='the part on which to perform the action. default = all')
    #tumme
    parser.add_argument('-b', '--board', action='store', required=False, default='all', 
                    choices=['all', 'ems4', 'mc4plus', 'mc2plus', 'mtb', 'mtb4', 'mtb4c','strain', 'strain2', 'strain2c', 'rfe', 'foc', 'foc-special', 'mc4', 'mais', 'bll', 'dsp', 'amc', 'amcbldc'],
                    help='the board on which to perform the action. default = all')
    parser.add_argument('-xb', '--excludeboard', action='store', required=False, default='none', 
                    choices=['none', 'ems4', 'mc4plus', 'mc2plus', 'mtb', 'mtb4', 'mtb4c', 'strain', 'strain2', 'strain2c', 'rfe', 'foc', 'foc-special', 'mc4', 'mais', 'bll', 'dsp', 'amc', 'amcbldc'],
                    help='exclude a board on which to perform the action. default = none')
    parser.add_argument('-a', '--action', action='store', required=True, default='info', choices=['info', 'topology', 'query', 'verify', 'update', 'program', 'forcemaintenance', 'forceapplication'],
                    help='the action to perform on board(s) selected by --part and --board. ' +
                         'With info: details inside xml files are printed together with an estimate of programming time. ' +
                         'With topology: eth topology details inside xml files are printed. ' +
                         'With query: boards on the robot are asked about their running FW version. ' +
                         'With verify: boards on the robot are verified vs FW version specified inside the xml files. ' +
                         'With update: boards on the robot are programmed with the FW files specified by xml files only if their FW version is not aligned. ' +
                         'With program: boards on the robot are programmed with the FW files specified by xml files. ' +
                         'With forcemaintenance: boards on the robot are sent in maintenance mode. ' +
                         'With forceapplication: boards on the robot are sent in application mode. ')
    parser.add_argument('--parallel', action='store_true', default=False,
                    help='if set, perform parallel programming of boards using FirmwareUpdater CLI with multiple addresses')
    parser.add_argument("-d", "--debug", action="store_true", default=0,
                    help="enables debug mode. its use is reserved to developers and is hence undocumented. default = 0")


    args = parser.parse_args()  

    # print str(sys.argv[0:])

    # pass parameters to program

    _verbosity = args.verbosity
    _filerobot = args.network.name
    _fileboards = args.firmware.name
    _part = args.part
    _parallel = args.parallel
    # ...existing code...
    # ...existing code...
    _board = args.board
    _action = args.action
    _debugmode = args.debug
    _excludedboard = args.excludeboard


    import datetime

    # some warnings ...


    if _debugmode:
        print (pyprefix + '[warning] debugmode is enabled!')

    if _verbosity > 0:
        print (pyprefix + '[info] the script is executing')

    if 0 == _verbosity:
        _verbose = 0 
        _verbosityFU = 0
    elif 1 == _verbosity:
        print (pyprefix + "[info] verbosity turned on for basic python only" )
        _verbose = 1 
        _verbosityFU = 0
    elif 2 == _verbosity:
        print (pyprefix + "[info] verbosity turned on for full python only" )
        _verbose = 2 
        _verbosityFU = 0
    else: 
        print (pyprefix + "[info] verbosity turned on for full python and FirmwareUpdater" )
        _verbose = 3 
        _verbosityFU = 1


    # get the current date and time

    start_time = datetime.datetime.now()
    print(start_time)


    # open the xml files: one for robot description and one for board properties
    
    import xml.etree.ElementTree as ET
    xmltreeOfRobot = ET.parse(_filerobot)
    xmlrootOfRobot = xmltreeOfRobot.getroot()
    xmltreeOfBoards = ET.parse(_fileboards)
    xmlrootOfBoards = xmltreeOfBoards.getroot()



    # so far so good: now execute the action

    if _action == 'info':
        r = info(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'query':
        r = query(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'verify':
        r = verify(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'program':
        r = program(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'update':
        r = update(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'forcemaintenance':
        r = maintenance(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'forceapplication':
        r = application(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    elif _action == 'topology':
        r = topology(_part, _board, xmlrootOfRobot, xmlrootOfBoards, _verbose)
    else:
        print (pyprefix + '[error] unsupported action: ' + _action)


    if _verbosity > 0:
        print (pyprefix + '[info] the script is over')


    # get the current date and time
    end_time = datetime.datetime.now()
    print(end_time)
    # print the time difference
    duration = end_time - start_time
    print(f"Total execution time: {duration}")

