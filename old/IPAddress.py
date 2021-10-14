# Copyright (c)  Maen Artimy


import math

class IPAddress4(object):

    def __init__(self, addr, mask):
        self.addr = addr
        self.mask = mask

    def __str__(self):
        b = self.addr
        m = self.mask
        lst0 = b & 255
        lst1 = b >> 8 & 255
        lst2 = b >> 16 & 255
        lst3 = b >> 24 & 255
        addr_str = '.'.join(str(i) for i in [lst3, lst2, lst1, lst0])
        addr_str += '/' + str(bin(m).count('1'))
        return addr_str

    @staticmethod
    def parseIPAddr4(net):
        addr = net.split('/')
        octets = addr[0].split('.')

        if len(addr) > 2:
            raise ValueError
        if len(octets) != 4:
            raise ValueError

        masklen = int(addr[1])
        if masklen < 0 or masklen > 32:
            raise ValueError

        dec = 0
        for i in range(4):
            octdec = int(octets[i])
            if octdec < 0 or octdec > 255:
                raise ValueError
            else:
                dec += 256 ** (3 - i) * octdec

        mask = int('0b' + '1' * masklen + '0' * (32 - masklen), 2)

        return  IPAddress4(dec, mask)

if __name__ == '__main__':
    net_addr = IPAddress4.parseIPAddr4('192.168.64.5/19')
    print(net_addr)