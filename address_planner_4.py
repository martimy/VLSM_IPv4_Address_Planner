# =============================================================================
# Copyright 2022 Maen Artimy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
An VLSM address planner for IPv4
"""

import math
import ipaddress
from binpackmod import BinPack


class AddressPlan4():
    """
    IPv4 address planner using VLSM
    """

    class __Results():
        """
        Encapsulates the planner results
        """

        def __init__(self, labels, req, hosts, net_addresses):
            self.net_addresses = net_addresses
            self.result = zip(labels, req, hosts, net_addresses)

        def get_output(self):
            """
            return address plan as a string
            """
            line_seperator = "=" * 52
            lines = []
            lines.append(line_seperator)
            lines.append(
                f"{'Label':<16} {'Required':<10} {'Free':<6} {'Assigned':<20}")
            lines.append(line_seperator)
            for r in self.result:
                lines.append(
                    f'{r[0]:<16} {r[1]:<10} {(r[2] - r[1]):<6} {r[3]:<20}')
            lines.append(line_seperator)
            return "\n".join(lines)

    def __init__(self, requirements, scale=1.0):
        # Sort the requirements dictionary
        s_req = dict(sorted(requirements.items(),
                     key=lambda item: item[1], reverse=True))
        self.labels = list(s_req.keys())
        self.req = list(s_req.values())
        self.scale = scale

        self.mask_len = 0
        self.utilization = 0
        self.blocks = []
        self.block_size = 0
        self.block_offset = 0

    def plan(self, prefix, method="FIRST"):
        """
        create an address plan
        """

        # Get the number of bits needed for each subnet in requirements
        bits = [math.ceil(math.log(r * self.scale + 2, 2)) for r in self.req]

        # Get the int value of the address and its mask length
        # This will raise an exception if the prefix is not formatted properly
        x = ipaddress.ip_network(prefix)
        addr_int_value, self.mask_len = int(x.network_address), x.prefixlen

        # Get a list of the mask bit extensions needed to split the network
        # prefix, and the number of available subnets using mask extention
        bit_ext = self.__get_mask_ext(bits, self.mask_len)
        num_subnets = self.__get_subnets(bit_ext)
        self.utilization = self.__get_utilization(num_subnets)
        if (min(bit_ext) < 0) or (self.utilization > 1):
            raise ValueError('Insufficient space!')

        # Get size of a single address block using the maximum number of
        # subnets needed
        self.blocks = [max(num_subnets) // i for i in num_subnets]

        # Use BinPack algorithm to assign subnets from the main prefix
        # The algorithm needs number of bins and a bin size
        # The algorithm has three variations "FIRST", "BEST", and "WORST"
        # to assign address blocks to bins
        # each bin represents a major subnet of the main prefix
        # while the size of the bin represents the number of available
        # subnets withing the main subnet resulting in variable length
        # subnet allocation
        num_bins = min(num_subnets)
        bin_size = max(self.blocks)
        bin_pack = BinPack(num_bins, bin_size)
        fitted = bin_pack.fit(self.blocks, method)

        # flatten the bin positions
        bin_positions = [p[0] * bin_size + p[1] for p in fitted]

        # convert the bin positions to block offsets
        self.block_size = 2 ** min(bits)
        self.block_offset = [i * self.block_size for i in bin_positions]

        # get the subnet prefixes by adding the integer value of the main
        # prefix to the block offsets from the Bin Pack algorithm
        # get the subnet mask len by adding bit extension to the original
        # mask length.
        # convert the two number to a string representing the subnet address
        net_addresses = [self.__addr_to_str(
            addr_int_value + k[0], self.mask_len + k[1])
            for k in zip(self.block_offset, bit_ext)]

        # get avaible ip addresses in each subnet
        hosts = [2 ** b - 2 for b in bits]

        return self.__Results(self.labels, self.req, hosts, net_addresses)

    def __addr_to_str(self, b, m):
        return f"{ipaddress.IPv4Address(b).exploded}/{m}"

    def __get_mask_ext(self, bits, mask_len):
        """
        get the number of bits needed for subnetting
        """
        return [32 - mask_len - n for n in bits]

    def __get_subnets(self, ext):
        """
        get the number of subnets for each mask extension
        """
        # total = sum([1 / n for n in num_subnets])
        return [2 ** n for n in ext]

    def __get_utilization(self, num_subnets):
        return sum([1 / n for n in num_subnets])

    def get_map(self):
        """
        get the address allocation map as a string
        """
        total = 2 ** (32 - self.mask_len)
        offset = [i//self.block_size for i in self.block_offset]

        output = f"Total available addresses: {total}\n"
        output += f"Allocated blocks: {self.blocks}\n"
        output += f"Block size: {self.block_size}\n"
        output += f"Offset: {offset}\n"
        output += "Legend: (#) Allocated block, (-) Free block\n"
        num_blocks = total // self.block_size
        tiles = "-" * num_blocks

        count = len(offset)
        for i in range(count):
            s_str = tiles[0:offset[i]] + "#" * self.blocks[i]
            tiles = s_str + tiles[len(s_str):]
        output += tiles
        return output


if __name__ == '__main__':

    NETWORK = '10.10.0.0/21'
    req_subnets = {'A': 177, 'B': 160, 'C': 50,
                   'D': 62, 'E': 123, 'F': 104, 'G': 67, 'H': 67}
    plan = AddressPlan4(req_subnets)
    result = plan.plan(NETWORK)
    print(result.get_output())
    print()
    print(plan.get_map())
