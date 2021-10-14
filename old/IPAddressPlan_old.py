import math
from binpackmod import BinPack


class AddressPlan4(object):
    # def run_old(self, network, orig, growth=1.0):
    #     req, labels = self.__sort_req(orig)
    #     bits = self.__bits_needed(req, growth)
    #
    #     # get the network address as a list then convert it to decimal
    #     netaddr, mask = self.__addr_to_list(network)
    #     h, c, t = self.__check(bits, mask)
    #     if h is None:
    #         raise ValueError('Network mask is too short!')
    #
    #     # From IP dotted decimal string to binary string
    #     # print(''.join([bin(int(x) + 256)[3:] for x in network.split('.')]))
    #
    #     bin_value = int(sum([256 ** (3 - y) * netaddr[y] for y in range(4)]))
    #
    #     # From IP decimal to binary string
    #     # print("{0:032b}".format(bin_value))
    #
    #     # Size of blocks relative to the smallest block
    #     u = [c[-1] // i for i in c]
    #     u_size = 2 ** bits[-1]
    #
    #     x = len(u)
    #     for k in range(x):
    #         print(labels[k], self.__addr_to_str(bin_value, mask + h[k]))
    #         bin_value += u_size * u[k]
    #
    # def __sort_req(self, req_list):
    #     s = sorted(req_list, key=lambda j: j[1], reverse=True)
    #     req = [i[1] for i in s]
    #     labels = [i[0] for i in s]
    #     return req, labels

    ###############################################################
    def run(self, network, org, growth=1.0):
        req, labels = self.__split_req(org)  # order the req and split them into values and labels
        bits = self.__bits_needed(req, growth)  # number of bits needed to fulfill the requirements

        bin_value, mask = self.__addr_to_dec(network)
        # return a list of the additional mask length needed to split the network address, and
        # the number of blocks available for each mask length
        h, c, t = self.__check(bits, mask)
        if h is None:
            raise ValueError('Network mask is too short!')

        # Size of blocks relative to the smallest block
        # these are the BinPack requirements
        u = [max(c) // i for i in c]  # c[-1] is the largest
        u_size = 2 ** min(bits)  # bits[-1] is the smallest

        bins = BinPack(min(c), max(u))  # Num. of bins and bin size (min c and max u)
        result, ignore = bins.fit(u)

        mult = [i * u_size for i in result]
        assgn = [self.__addr_to_str(bin_value + k[0], mask + k[1]) for k in zip(mult, h)]
        return zip(labels, req, [2 ** b - 2 for b in bits], assgn), t

    def __split_req(self, req_list):
        req = [i[1] for i in req_list]
        labels = [i[0] for i in req_list]
        return req, labels

    def __bits_needed(self, req, g):
        bits = []
        for r in req:
            n = math.ceil(math.log(r * g + 2, 2))
            bits.append(n)
        return bits

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
        # Check if the biggest subnet can be accommodated
        # Check if the total subnet sizes can be accommodated
        h = [32 - mask - m for m in bits]
        c = [2 ** i for i in h]

        total = sum([1 / i for i in c])
        if (h[0] < 0) or (total > 1):
            return None, None, None

        return h, c, total

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
    req_subnets = [('A', 1777), ('B', 1560), ('C', 500), ('D', 672), ('E', 123), ('F', 904), ('G', 677), ('H', 67)]


    plan = AddressPlan4()
    result, alloc = plan.run(network, req_subnets)
    AddressPlan4.display(result)

    network = '10.10.0.0/21'
    req_subnets = [('A', 177), ('B', 160), ('C', 50), ('D', 62), ('E', 123), ('F', 104), ('G', 67), ('H', 67)]

    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets)
    AddressPlan4.display(result)

    network = '192.168.16.0/19'
    req_subnets = [('Operations1', 2150), ('Operations2', 975), ('Operations3', 175), ('Sales', 575), ('DMZ', 5)]

    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets, growth=1.0)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))

    network = '192.168.0.0/16'
    req_subnets = [('B1_Legal', 120), ('B1_Acc', 370), ('B1_DMZ', 5),
                   ('B2_HQ', 1580), ('B2_Eng', 200), ('B2_DMZ', 5),
                   ('B3_Operations1', 2150), ('B3_Operations2', 975), ('B3_Operations3', 175), ('B3_Sales', 575), ('B3_DMZ', 5),
                   ('B4_Sales', 75), ('B4_Market', 75), ('B4_DMZ', 5),
                   ('B5_Sales', 80),
                   ('P2P', 10)]

    plan = AddressPlan4()
    #plan.run_old(network, req_subnets)
    result, alloc = plan.run(network, req_subnets, growth=1.0)
    AddressPlan4.display(result)
    print('Allocated = {:0.1f}'.format(alloc))
