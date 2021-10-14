import math
import sys


def sort_req(req_list):
    s = sorted(req_list, key=lambda j: j[1], reverse=True)
    req = [i[1] for i in s]
    labels = [i[0] for i in s]
    return req, labels


def bits_needed(req):
    bits = []
    for item in req:
        n = math.ceil(math.log(item + 2, 2))
        bits.append(n)
    return bits


# Take a string representation of  network address and return
# list of four octets and a mask
def addr_to_list(net):
    addr = net.split('/')
    return [int(x) for x in addr[0].split('.')], int(addr[1])


def addr_to_str(b, m):
    lst0 = b & 255
    lst1 = b >> 8 & 255
    lst2 = b >> 16 & 255
    lst3 = b >> 24 & 255
    addr_str = '.'.join(str(i) for i in [lst3, lst2, lst1, lst0])
    addr_str += '/' + str(m)
    return addr_str


def check(bits, mask):
    # Check if the biggest subnet can be accommodated
    # Check if the total subnet sizes can be accommodated
    h = [32 - mask - m for m in bits]
    c = [2 ** i for i in h]

    total = sum([1 / i for i in c])
    if (h[0] < 0) or (total > 1):
        return None, None

    return h, c

def main(network, req_subnets):
    req, labels = sort_req(req_subnets)
    bits = bits_needed(req)

    # get the network address as a list then convert it to decimal
    netaddr, mask = addr_to_list(network)
    h, c = check(bits, mask)
    if h is None:
        raise ValueError('Network mask is too short!')

    # From IP dotted decimal string to binary string
    # print(''.join([bin(int(x) + 256)[3:] for x in network.split('.')]))

    binValue = int(sum([256 ** (3 - y) * netaddr[y] for y in range(4)]))

    # From IP decimal to binary string
    # print("{0:032b}".format(binValue))

    # Size of blocks relative to the smallest block
    u = [c[-1] // i for i in c]
    u_size = 2 ** bits[-1]

    addr = []
    ml = []
    x = len(u)
    for k in range(x):
        print(labels[k], addr_to_str(binValue, mask + h[k]))
        addr.append(binValue)
        ml.append(mask + h[k])
        binValue += u_size * u[k]

if __name__ == '__main__':
    network = '192.168.128.0/19'
    req_subnets = [('A', 1777), ('B', 1560), ('C', 500), ('D', 672), ('E', 123), ('F', 904), ('G', 677), ('H', 67)]
    try:
        main(network, req_subnets)
    except ValueError as e:
        print(e)

