#!/usr/bin/python3

# import config
import getopt
import json
import socket
import struct
import sys

from time import sleep

UDP_IP = '127.0.0.1'
UDP_PORT = 30001
BUFFERSIZE = 880
JSON_FILE = 'config.json'
KEYS = [ 'byte_index', 'short_name', 'type', 'description', 'matrix_group' ]

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


def _ReadJSONFile(filename):
    try:
        with open('config.json', 'r') as fd:
            data_dict = json.load(fd)
        fd.close()

    except:
        print('Error on opening file')
        sys.exit(1)
    
    return data_dict


def event_loop():
    # TODO:
    # - Split the UDP-importer and printing of data over 2 threads or use async. (not sure if this is a good stategy)
    # - Record to and playback from file.
    count = 0    
    udp_importer = UDP_Importer()
    
    print('Stats-display started.')

    while True:
        udp_importer.ReceiveAndPut()
        
        if count == 5:
            udp_importer.PrintStats()
            count = 0
        
        else:
            count += 1


class Motorcycle(object):
    def __init__(self, blueprint):
        self.attribute_list = []
        self._CreateAttributes(blueprint)
    
    def __str__(self):
        to_print = ''

        for key in self.attribute_list:
            stat = config.PACKET_BLUEPRINT[key][1]
            stat_value = str(getattr(self, key))
            tab_spaces = self._len_longest_key - len(stat)
            padding_spaces = 30 - len(stat)
            tabulator = _Spacer(tab_spaces)
            padding = _Spacer(padding_spaces)

            to_print += f'{stat}{tabulator} : {stat_value}{padding}\n'
            
        return to_print
    
    def _CreateAttributes(self, blueprint):
        len_longest_key = 0
                
        for key in blueprint:
            value_list = [ None for _ in range(len(KEYS)) ]
            
            for attribute in blueprint[key]:
                if KEYS.count(attribute):
                    idx = KEYS.index(attribute)
                    value_list[idx] = blueprint[key][attribute]

            key_length = len(value_list[1])
                
            if key_length > len_longest_key:
                len_longest_key = key_length
            
            setattr(self, key, value_list)
            self.attribute_list.append(key)
            # print(f'{key}: {value_list}') 

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
    def __init__(self, cli_args=None):
        self._UDPClientSocket = socket.socket(socket.AF_INET,
                                              socket.SOCK_DGRAM)
        self._UDPClientSocket.bind((UDP_IP, UDP_PORT))
        self._blueprint = _ReadJSONFile(JSON_FILE)
        self.mc = Motorcycle(self._blueprint)

    def _UnpackPacket(self, raw_packet):
        # When outside of simulaton, skip
        if struct.unpack_from('i', raw_packet, offset=4)[0] == 0:
            return None
        
        packet_data = {}
        
        for key in self._blueprint:
            key_type = self._blueprint[key]['type']
            
            # See https://docs.python.org/3/library/struct.html#format-characters
            # for Format Characters / fmt_char.
            if key_type == 'int':
                fmt_char = 'i'
                
            elif key_type == 'str':
                fmt_char = 's'
                
            elif key_type == 'float':
                fmt_char = 'f'
            
            offset = self._blueprint[key]['byte_index']
            value = struct.unpack_from(fmt_char, raw_packet, offset=offset)
            packet_data[key] = value[0]
            
        return packet_data
    
    def _GetPacket(self):
        return self._UDPClientSocket.recvfrom(BUFFERSIZE)[0]
    
    def ReceiveAndPut(self):
        raw_packet = self._GetPacket()
        self.mc.UpdateAttributes(self._UnpackPacket(raw_packet))
        
    def PrintStats(self):
        rows_amount = len(self.mc.attribute_list)
        
        cursor_ups = _ConsoleCursorUps(rows_amount)
        print(f'{str(self.mc)}{cursor_ups}')


def main(argv):
    try:
        opts, unused_args = getopt.getopt(argv, 'i:')
   
    except getopt.GetoptError:
        # TODO: Improve this error
        print ('Bad command-line attributes')
        sys.exit(2)

    if opts:
        global UDP_IP, UDP_PORT
        UDP_IP, port = opts[0][1].split(':')
        UDP_PORT = int(port)
        
        print(f'Serving at: {UDP_IP}:{UDP_PORT}')
        
    try:
        event_loop()
    
    except KeyboardInterrupt:
        print('\nStats-display interrupted, exiting program.')


if __name__ == '__main__':
    main(sys.argv[1:])
