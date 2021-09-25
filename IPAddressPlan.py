import math
from binpackmod import BinPack
import ipaddress

class AddressPlan4(object):

    def run(self, network, org, growth=1.0):
        # Sort the requirements
        s = {k: v for k, v in sorted(org.items(), key=lambda item: item[1], reverse=True)}
        labels = list(s.keys())
        req = list(s.values())
        
        # Get the number of bits needed to fulfill the requirements
        bits = [math.ceil(math.log(r * growth + 2, 2)) for r in req]

        # Get the int value of the address and its mask length
        x = ipaddress.ip_network(network)
        int_value, mask = int(x.network_address), x.prefixlen
                
        # return a list of the mask extensions needed to split the network 
        # address, and the number of address blocks available for each mask 
        # length
        ext_bits, num_subnets, utilization = self.__get_subnets(bits, mask)
        if (min(ext_bits) < 0) or (utilization > 1):
            raise ValueError('Network mask is too short!')

        # Ratio of blocks relative to the smallest block
        # these are the BinPack requirements
        self.blocks = [max(num_subnets) // i for i in num_subnets]
        num_bins = min(num_subnets)
        bin_size = max(self.blocks)
        
        bins = BinPack(num_bins, bin_size)
        fitted = bins.fit(self.blocks)
        
        # maps the positions in bins to offset numbers
        result = [k[0] * bin_size + k[1] for k in fitted]
        self.total = 2 ** (32-mask)

        # convert the position offests to bits offsets
        self.block_size = 2 ** min(bits)      
        self.mult = [i * self.block_size for i in result]

        assgn = [self.__addr_to_str(int_value + k[0], mask + k[1]) for k in zip(self.mult, ext_bits)]
        return zip(labels, req, [2 ** b - 2 for b in bits], assgn, self.mult), utilization

    
    def __addr_to_str(self, b, m):
        return f"{ipaddress.IPv4Address(b).exploded}/{m}"

    def __get_subnets(self, bits, mask_len):
        """
        get the number of bit needed for subnetting and the number of 
        resultant subnets.
        """
        
        ext_bits = [32 - mask_len - n for n in bits]
        num_subnets = [2 ** n for n in ext_bits]
        total = sum([1 / n for n in num_subnets])

        return ext_bits, num_subnets, total

    def get_map(self):
        offset = [i//self.block_size for i in self.mult]
        print("Total:", self.total, ", Blocks:", self.blocks)        
        print("Block size:", self.block_size, ", Offset:", offset)
        
        num_blocks = self.total // self.block_size
        tiles = "-" * num_blocks
        
        count = len(offset)
        for i in range(count):
            s_str = tiles[0:offset[i]] + "#" * self.blocks[i]
            tiles =  s_str + tiles[len(s_str):]
        print(tiles)
        
        
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
    plan.get_map()
    
    network = '10.10.0.0/21'
    req_subnets = {'A': 177, 'B': 160, 'C': 50, 'D': 62, 'E': 123, 'F': 104, 'G': 67, 'H': 67}
        
    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets)
    AddressPlan4.display(result)
    plan.get_map()
    
    network = '192.168.32.0/19'
    req_subnets = {'Operations1': 2150, 'Operations2': 975, 'Operations3': 175, 'Sales': 575, 'DMZ': 5}

    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets, growth=1.0)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))
    plan.get_map()
    
    network = '192.168.0.0/18'
    req_subnets = {'B1_Legal': 120, 'B1_Acc': 370, 'B1_DMZ': 5, 'B2_HQ': 1580, 'B2_Eng': 200, 'B2_DMZ': 5,
                   'B3_Operations1': 2150, 'B3_Operations2': 975, 'B3_Operations3': 175, 'B3_Sales': 575, 'B3_DMZ': 5,
                   'B4_Sales': 75, 'B4_Market': 75, 'B4_DMZ': 5, 'B5_Sales': 80, 'P2P': 10}

    plan = AddressPlan4()
    result, alloc = plan.run(network, req_subnets, growth=1.0)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))
    plan.get_map()
    
    network = '192.168.4.0/24'
    req_subnets = {'A': 72, 'B': 15, 'C': 15, 'D': 6}

    plan = AddressPlan4()
    result, alloc = plan.run(network, req_subnets, growth=1.5)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))
    plan.get_map()
    