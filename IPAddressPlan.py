import math
from binpackmod import BinPack


class AddressPlan4(object):

    def run(self, network, org, growth=1.0):
        labels = list(org.keys())
        req = list(org.values())
        # Get the number of bits needed to fulfill the requirements
        bits = [math.ceil(math.log(r * growth + 2, 2)) for r in req]

        bin_value, mask = self.__addr_to_dec(network)
        # return a list of the mask extensions needed to split the network address, and
        # the number of address blocks available for each mask length
        ext, blocks, utilization = self.__check(bits, mask)
        if ext is None:
            raise ValueError('Network mask is too short!')

        # Ratio of blocks relative to the smallest block
        # these are the BinPack requirements
        u = [max(blocks) // i for i in blocks]
        u_size = 2 ** min(bits)

        bins = BinPack(min(blocks), max(u))  # Num. of bins and bin size (min c and max u)
        result, _ = bins.fit(u)

        mult = [i * u_size for i in result]
        assgn = [self.__addr_to_str(bin_value + k[0], mask + k[1]) for k in zip(mult, ext)]
        return zip(labels, req, [2 ** b - 2 for b in bits], assgn), utilization


    def __addr_to_dec(self, netstr):
        # get the network address as a list of four decimal values
        addrlist, mask = self.__addr_to_list(netstr)
        dec = int(sum([256 ** (3 - y) * addrlist[y] for y in range(4)]))
        return dec, mask

    # Take a string representation of  network address and return
    # list of four decimals and a mask
    def __addr_to_list(self, net):
        addr = net.split('/')
        return [int(x) for x in addr[0].split('.')], int(addr[1])

    def __addr_to_str(self, b, m):
        lst0 = b & 255
        lst1 = b >> 8 & 255
        lst2 = b >> 16 & 255
        lst3 = b >> 24 & 255
        addr_str = '.'.join(str(i) for i in [lst3, lst2, lst1, lst0])
        addr_str += '/' + str(m)
        return addr_str

    def __check(self, bits, mask):
        '''
           Check if the biggest subnet can be accommodated
           Check if the total subnet sizes can be accommodated
        '''
        ext = [32 - mask - m for m in bits]
        blocks = [2 ** i for i in ext]
        total = sum([1 / i for i in blocks])
        if (min(ext) < 0) or (total > 1):
            return None, None, None

        return ext, blocks, total

    @staticmethod
    def display(result):
        print("=" * 52)
        print("{0:<16} {1:<6} {2:<6} {3:<20}".format('Label', 'Req', 'Avail', 'Assigned'))
        print("=" * 52)
        for r in result:
            print('{0:<16} {1:<6} {2:<6} {3:<20}'.format(r[0], r[1], (r[2] - r[1]), r[3]))
        print("=" * 52)


if __name__ == '__main__':
    network = '192.168.64.0/19'
    req_subnets = {'A': 1777, 'B': 1560, 'C': 500, 'D': 672, 'E': 123, 'F': 904, 'G': 677, 'H': 67}
    

    plan = AddressPlan4()
    result, alloc = plan.run(network, req_subnets)
    AddressPlan4.display(result)

    network = '10.10.0.0/21'
    req_subnets = {'A': 177, 'B': 160, 'C': 50, 'D': 62, 'E': 123, 'F': 104, 'G': 67, 'H': 67}
        
    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets)
    AddressPlan4.display(result)

    network = '192.168.16.0/19'
    req_subnets = {'Operations1': 2150, 'Operations2': 975, 'Operations3': 175, 'Sales': 575, 'DMZ': 5}

    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets, growth=1.0)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))

    network = '192.168.0.0/18'
    req_subnets = {'B1_Legal': 120, 'B1_Acc': 370, 'B1_DMZ': 5, 'B2_HQ': 1580, 'B2_Eng': 200, 'B2_DMZ': 5,
                   'B3_Operations1': 2150, 'B3_Operations2': 975, 'B3_Operations3': 175, 'B3_Sales': 575, 'B3_DMZ': 5,
                   'B4_Sales': 75, 'B4_Market': 75, 'B4_DMZ': 5, 'B5_Sales': 80, 'P2P': 10}

    plan = AddressPlan4()
    result, alloc = plan.run(network, req_subnets, growth=1.0)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))
