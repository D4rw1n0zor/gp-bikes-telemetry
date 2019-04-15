#!/usr/bin/python3

import socket
import sys
import struct
import os
import config
from os import system, name 
import colorama
colorama.init()

from time import sleep


def _ConsoleCursorUps(rows_amount):
    cursor_ups_string = ''
    c = 0
    
    while c <= rows_amount:
        cursor_ups_string += '\033[A\033[G'
        c += 1
        
    return cursor_ups_string


def _Spacer(spaces):
    space_str = ''
    c = 0
    
    while c < spaces:
        space_str += ' '
        c += 1
        
    return space_str

    
def event_loop():
    # TODO:
    # - Split the UDP-importer and printing of data over 2 threads or use async.
    # - Record to and playback from file.
    count = 0    
    udp_importer = UDP_Importer()
    print('Stats-display started.')

    while True:
        udp_importer.ReceiveAndPut()
        
        if count == 5:
            udp_importer.PrintStats()
            count = -1
        
        count += 1


class Motorcycle(object):
    def __init__(self, blueprint):
        self.attribute_list = []
        self._CreateAttributes(blueprint)
    
    def __str__(self):
        to_print = ''

        for key in self.attribute_list:
            stat = config.PACKET_BLUEPRINT[key][1]
            
            stat_value = getattr(self, key)
            
            if isinstance(stat_value, float):
               stat_value = '%.2f' % (stat_value)
            
            tab_spaces = self._len_longest_key - len(stat)
            padding_spaces = 30 - len(stat) # 
            tabulator = _Spacer(tab_spaces)
            padding = _Spacer(padding_spaces)

            to_print += f'{stat}{tabulator} : {stat_value}{padding}\n'
            
        return to_print
    
    def _CreateAttributes(self, blueprint):
        len_longest_key = 0
        
        for key in blueprint:
            key_type = blueprint[key][2]
            key_length = len(blueprint[key][1])
                
            if key_length > len_longest_key:
                len_longest_key = key_length
            
            setattr(self, key, None)
            self.attribute_list.append(key)

        self._len_longest_key = len_longest_key 
            
    def GetData(self):
        pass
    
    def UpdateAttributes(self, packet_data):
        if not packet_data:
            return

        for key in packet_data:
            value = packet_data[key]
            
            setattr(self, key, value)


class UDP_Importer(object):
    def __init__(self):
        self._blueprint = config.PACKET_BLUEPRINT
        self._UDPClientSocket = socket.socket(socket.AF_INET,
                                              socket.SOCK_DGRAM)
        self._UDPClientSocket.bind((config.UDP_IP,
                                    config.UDP_PORT))
        self.mc = Motorcycle(self._blueprint)
    
    def _UnpackPacket(self, raw_packet):
        # When outside of simulaton, skip
        if struct.unpack_from('i', raw_packet, offset=4)[0] == 0:
            return None
        
        packet_data = {}
        
        for key in self._blueprint:
            key_type = self._blueprint[key][2]
            
            ''' See https://docs.python.org/3/library/struct.html#format-characters
            for Format Characters / fmt_char.
            int -> i
            str -> s
            float -> f
            '''
            fmt_char = key_type[0];
            #print(key_type[0])
            # Exception if we meet an array
            if key_type == 'f_array':
                offset = self._blueprint[key][0]
                value = ""
                y = 0
                while(y < int(self._blueprint[key][6],10)):
                    value += '[ '
                    x = 0
                    while (x < int(self._blueprint[key][5],10)):
                        temp_value = struct.unpack_from(fmt_char, raw_packet, offset=offset)
                        value += '%.2f ' % (temp_value)
                        value += '\t'
                        offset += 4
                        x += 1
                    value += ']\n                               ' 
                    ### TODO We should dynamically add some padding here
                    y += 1
                packet_data[key] = value
            else:
                offset = self._blueprint[key][0]
                value = struct.unpack_from(fmt_char, raw_packet, offset=offset)
                packet_data[key] = value[0]

        return packet_data
    
    def _GetPacket(self):
        # recvfrom returns a 2-tuple value: data + server address
        return self._UDPClientSocket.recvfrom(config.BUFFERSIZE)[0]
    
    def ReceiveAndPut(self):
        raw_packet = self._GetPacket()
        self.mc.UpdateAttributes(self._UnpackPacket(raw_packet))
        
    def PrintStats(self):
        #print("print stats!")
        rows_amount = len(self.mc.attribute_list)+8 # as the matrix is actually 9 lines
        cursor_ups = _ConsoleCursorUps(rows_amount)
        print(str(self.mc) + cursor_ups)


def main():
    # define our clear function
    def clear(): 
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 
    clear()
    try:
        event_loop()
    
    except KeyboardInterrupt:
        print('\nStats-display interrupted, exiting program.')


if __name__ == '__main__':
    main()
