This is a complete app to automatically create an IPAdderss plan for a network


# VLSM (CIDR) Subnet Calculator

Variable Length Subnet Masking is a technique that allows network designer to 
divide an IP address space to subnets of different sizes, 
unlike simple same-size subnetting. 

This app is intend to automate and simplify VLSM calculation process.

# How to use

Provide major network prefix and mask, e,g. 192.168.1.0/24
Provide sizes (number of assignable ip addresses) of required subnets.


# Algorithm

Input: 

- Main Network Prefix
- Requirements (number of hosts in each subnet)
- Growth factor

1. Get the number of bits required for each subnet
2. Get the mask extension needed for each requirements
3. Get the number of subnets that result from 2
4. Check of the requirements can be accomodated
5. Calaculate the size of blocks 
6. Use the maximum subnet size as unit to determine the Bin size and 
7. Use Bin Pack Algorithm to get block to bin assignment
8. Assign network addresses


# Example:

Say you are give the prefix 192.168.4.0/24
and asked to subnet it to networks of 72, 15, and 6 hosts each (ignore growth).

1. The required bits for each: 7, 5, 3
2. 32-24-7 = 1, 32-24-5 = 3, 32-24-3 = 5
3. num_subnets = 2, 8, 32
4. Utilization = 1/2+1/8+1/32 = 0.65625
5. blocks = [32/2, 32/8, 32/32] = [16, 4, 1]
6. num_bins = min(num_subnets) = 2
   bin_size = max(blocks) = 16
7. fitted = [(0,0), (1,0), (1,4)]
   result = [0, 16, 20]
8. block size = 2^3 = 8
   mult = [0, 128, 160]
   ext_bits = [1, 3, 5]
   
9. 192.168.4.0 + 0 / 25
   192.168.4.0 + 128 / 27
   192.168.4.0 + 160 / 29
   