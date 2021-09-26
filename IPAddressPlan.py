import math
from binpackmod import BinPack
import ipaddress


class AddressPlan4(object):

    class __Results(object):

        def __init__(self, labels, req, hosts, netAddresses):
            self.netAddresses = netAddresses
            self.result = zip(labels, req, hosts, netAddresses)

        def getOutput(self):
            SEP = "=" * 52
            lines = []
            lines.append(SEP)
            lines.append("{0:<16} {1:<6} {2:<6} {3:<20}".format(
                'Label', 'Req', 'Avail', 'Assigned'))
            lines.append(SEP)
            for r in self.result:
                lines.append('{0:<16} {1:<6} {2:<6} {3:<20}'.format(
                    r[0], r[1], (r[2] - r[1]), r[3]))
            lines.append(SEP)
            return "\n".join(lines)

    def __init__(self, requirements, scale=1.0):
        # Sort the requirements dictionary
        s = {k: v for k, v in sorted(
            requirements.items(), key=lambda item: item[1], reverse=True)}
        self.labels = list(s.keys())
        self.req = list(s.values())
        self.scale = scale

    def plan(self, prefix, method="FIRST"):
        # Get the number of bits needed for each subnet in requirements
        bits = [math.ceil(math.log(r * self.scale + 2, 2)) for r in self.req]

        # Get the int value of the address and its mask length
        # This will raise an exception if the prefix is not formatted properly
        x = ipaddress.ip_network(prefix)
        addrIntValue, self.maskLen = int(x.network_address), x.prefixlen

        # Get a list of the mask bit extensions needed to split the network
        # prefix, and the number of available subnets using mask extention
        bitExt = self.__getMaskExt(bits, self.maskLen)
        numSubnets = self.__getSubnets(bitExt)
        self.utilization = self.__getUtilization(numSubnets)
        if (min(bitExt) < 0) or (self.utilization > 1):
            raise ValueError('Insufficient space!')

        # Get size of a single address block using the maximum number of
        # subnets needed
        self.blocks = [max(numSubnets) // i for i in numSubnets]

        # Use BinPack algorithm to assign subnets from the main prefix
        # The algorithm needs number of bins and a bin size
        # The algorithm has three variations "FIRST", "BEST", and "WORST"
        # to assign address blocks to bins
        # each bin represents a major subnet of the main prefix
        # while the size of the bin represents the number of available
        # subnets withing the main subnet resulting in variable length
        # subnet allocation
        num_bins = min(numSubnets)
        bin_size = max(self.blocks)
        binPack = BinPack(num_bins, bin_size)
        fitted = binPack.fit(self.blocks, method)

        # flatten the bin positions
        binPositions = [p[0] * bin_size + p[1] for p in fitted]

        # convert the bin positions to block offsets
        self.block_size = 2 ** min(bits)
        self.blockOffset = [i * self.block_size for i in binPositions]

        # get the subnet prefixes by adding the integer value of the main
        # prefix to the block offsets from the Bin Pack algorithm
        # get the subnet mask len by adding bit extension to the original
        # mask length.
        # convert the two number to a string representing the subnet address
        netAddresses = [self.__addrToStr(
            addrIntValue + k[0], self.maskLen + k[1]) 
            for k in zip(self.blockOffset, bitExt)]

        # get avaible ip addresses in each subnet
        hosts = [2 ** b - 2 for b in bits]

        return self.__Results(self.labels, self.req, hosts, netAddresses)

    def __addrToStr(self, b, m):
        return f"{ipaddress.IPv4Address(b).exploded}/{m}"

    def __getMaskExt(self, bits, maskLen):
        """
        get the number of bits needed for subnetting
        """
        return [32 - maskLen - n for n in bits]

    def __getSubnets(self, ext):
        """
        get the number of subnets for each mask extension
        """
        # total = sum([1 / n for n in num_subnets])
        return [2 ** n for n in ext]

    def __getUtilization(self, numSubnets):
        return sum([1 / n for n in numSubnets])

    def get_map(self):
        total = 2 ** (32 - self.maskLen)
        offset = [i//self.block_size for i in self.blockOffset]
        print("Total:", total, ", Blocks:", self.blocks)
        print("Block size:", self.block_size, ", Offset:", offset)

        num_blocks = total // self.block_size
        tiles = "-" * num_blocks

        count = len(offset)
        for i in range(count):
            s_str = tiles[0:offset[i]] + "#" * self.blocks[i]
            tiles = s_str + tiles[len(s_str):]
        print(tiles)


if __name__ == '__main__':
    network = '192.168.64.0/19'
    req_subnets = {'A': 1777, 'B': 1560, 'C': 500,
                   'D': 672, 'E': 123, 'F': 904, 'G': 677, 'H': 67}
    plan = AddressPlan4(req_subnets)
    result = plan.plan(network)
    print(result.getOutput())
    plan.get_map()

    network = '10.10.0.0/21'
    req_subnets = {'A': 177, 'B': 160, 'C': 50,
                   'D': 62, 'E': 123, 'F': 104, 'G': 67, 'H': 67}
    plan = AddressPlan4(req_subnets)
    #plan.plan_old(network, req_subnets)
    result = plan.plan(network)
    print(result.getOutput())
    plan.get_map()

    network = '192.168.32.0/19'
    req_subnets = {'Operations1': 2150, 'Operations2': 975,
                   'Operations3': 175, 'Sales': 575, 'DMZ': 5}
    plan = AddressPlan4(req_subnets, scale=1.0)
    #plan.plan_old(network, req_subnets)
    result = plan.plan(network)
    print(result.getOutput())
    # print('Allocated = {:0.1f}'.format(alloc))
    plan.get_map()

    network = '192.168.0.0/18'
    req_subnets = {'B1_Legal': 120, 'B1_Acc': 370, 'B1_DMZ': 5, 'B2_HQ': 1580, 
                   'B2_Eng': 200, 'B2_DMZ': 5, 'B3_Operations1': 2150, 
                   'B3_Operations2': 975, 'B3_Operations3': 175, 
                   'B3_Sales': 575, 'B3_DMZ': 5, 'B4_Sales': 75, 
                   'B4_Market': 75, 'B4_DMZ': 5, 'B5_Sales': 80, 'P2P': 10}
    plan = AddressPlan4(req_subnets, scale=1.0)
    result = plan.plan(network)
    print(result.getOutput())
    # print('Allocated = {:0.1f}'.format(alloc))
    plan.get_map()

    network = '192.168.2.0/24'
    req_subnets = {'A': 56, 'B': 15, 'C': 15, 'D': 4, 'E': 4, 'F': 4}
    plan = AddressPlan4(req_subnets, scale=1.0)
    result = plan.plan(network, method="WORST")
    print(result.getOutput())
    # print('Allocated = {:0.1f}'.format(alloc))
    plan.get_map()
