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


import os

# it retrieves arguments, such as ... TBD
def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            argv = argv[1:]
    return opts


# it retrieves properties of a given board
def get_board_properties(brdtype):
    prop = {}
    prptree = ET.parse('propertiesOfBoards.xml')
    prproot = prptree.getroot()
    for p in prproot.findall('board'):
        if brdtype == p.get('type'):
            prop = p
    return prop


# FirmwareUpdater --nogui --force-eth-maintenance --device ETH --id eth1 --eth_board $ipaddress --verbosity $verbosity
# FirmwareUpdater --nogui --force-eth-application --device ETH --id eth1 --eth_board $ipaddress --verbosity $verbosity
# FirmwareUpdater --nogui --program --device ETH --id eth1 --eth_board $ipaddress --file ${mapofboards[$boardtag]} --verbosity $verbosity
# FirmwareUpdater --nogui --program --device ETH --id eth1 --eth_board $ipaddress --can_line $canline --can_id $canid --file ${mapofboards[$boardtag]} --verbosity $verbosity

# select what kind of fw update to do: eth, eth:can, cfw2
def do_firmware_update(brd, prp):

    ondevice = brd.find('ondevice').text
    adr = brd.find('ataddress').attrib

    if 'ETH' == ondevice:
        if 0 == adr.get('canbus', 0):
            r = do_firmware_update_eth(brd, prp)
        elif 0 != adr.get('canadr', 0):
            r = do_firmware_update_canovereth(brd, prp)
        else:
            print 'the device ' + ondevice + ' with CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ' is unsupported: i quit!'
            r = 1;        
    elif 'CFW' == ondevice:
        r = do_firmware_update_cfw(brd, prp)
    else:
        print 'the device ' + ondevice + ' is unsupported: i quit!'
        r = 1;

    return r


def do_firmware_update_cfw(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    print 'cfw: performing fw update on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')
    print 'TO BE DONE'
    return 1

def do_firmware_update_canovereth(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    print 'canovereth: performing fw update on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')

    print 'step1: sending eth board in maintenance mode'
    command = 'FirmwareUpdater --nogui --force-eth-maintenance --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip') + ' --verbosity 0'
    print command 
    r = os.system(command)

    if 0 != r:
        print 'failed sending in maintenance mode eth board @ ' + adr.get('ip') + ': quitting!'
        return r   

    print 'step2: uploading can firmware'
    tmp1 = 'FirmwareUpdater --nogui --program --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip')
    tmp2 = ' --can_line ' + adr.get('canbus', '0') + ' --can_id ' + adr.get('canadr', '0') + ' --file ' + fw.find('file').text + ' --verbosity 1'
    command = tmp1 + tmp2
    print command 
    r = os.system(command)

    if 0 != r:
         print 'failed programming can board @ ' + adr.get('ip') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0') + ': quitting!'
         return r 


    print 'done!'

    return r


# it performs firmware update by calling the external program
def do_firmware_update_eth(brd, prp):
    r = 1
    adr = brd.find('ataddress').attrib
    fw = prp.find('firmware')
    print 'eth: performing fw update on board @ ' + adr.get('ip', '0') + ':CAN' + adr.get('canbus', '0') + ':' + adr.get('canadr', '0')

    print 'step1: sending eth board in maintenance mode'
    command = 'FirmwareUpdater --nogui --force-eth-maintenance --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip') + ' --verbosity 0'
    print command 
    r = os.system(command)

    if 0 != r:
        print 'failed sending in maintenance mode eth board @ ' + adr.get('ip') + ': quitting!'
        return r   

    print 'step2: uploading eth firmware'
    command = 'FirmwareUpdater --nogui --program --device ' + brd.find('ondevice').text + ' --id eth1 --eth_board ' + adr.get('ip') + ' --file ' + fw.find('file').text + ' --verbosity 0'
    print command 
    r = os.system(command)

    if 0 != r:
         print 'failed programming eth board @ ' + adr.get('ip') + ': quitting!'
         return r 


    print 'done!'

    return r




# main entrance
if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    if '-i' in myargs:
        print(myargs['-i'])
    print(myargs)

    # search for the xml file

    import xml.etree.ElementTree as ET
    brdtree = ET.parse('boardsOf.xml')
    brdroot = brdtree.getroot()
#    for child in brdroot:
#        print child.tag, child.attrib

    for part in brdroot.findall('part'):
        print part.tag, part.attrib
        for brd in part.findall('board'):
            prp = get_board_properties(brd.get('type'))
            # now: use brd and prp to perform fw update
            r = do_firmware_update(brd, prp)

            if 0 != r:
                print 'failure: i quit!'
                exit()

            dev = brd.find('ondevice').text
            adr = brd.find('ataddress').attrib            
            fw = prp.find('firmware')

            print prp.get('type'), prp.get('type'), fw.find('file').text, fw.find('version').get('major'), fw.find('version').get('minor')
            print brd.get('type'), dev, adr.get('ip'), adr.get('canbus', '0'), adr.get('canadr', '0')






