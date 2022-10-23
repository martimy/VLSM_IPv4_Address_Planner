# VLSM_IPv4_Address_Planner

This is an app that creates an IPv4 Adderss plan using VLSM  

Variable Length Subnet Masking is a technique that allows dividing an
IP address space to subnets of different sizes unlike simple same-size subnetting.

# How to use

- Provide major network prefix and mask, e.g. 192.168.1.0/24
- Provide requirements (number of assignable ip addresses) in each subnet
- Scale factor (e.g. 1.1 adds 10\% of free addresses, default=1)

## Example

Input:  
- Main network prefix: 10.10.0.0/24
- Requirements: A: 177, B: 160, C: 50, D: 62, E: 123, F: 104, G: 67, H: 67
- Scale factor: 1.1

Output:  

Label | Required | Free | Assigned            
------|----------|------|-----------
A | 177 | 77 | 10.10.0.0/24        
B | 160 | 94 | 10.10.1.0/24        
E | 123 | 131 | 10.10.2.0/24        
F | 104 | 22 | 10.10.3.0/25        
G | 67 | 59 | 10.10.3.128/25      
H | 67 | 59 | 10.10.4.0/25        
D | 62 | 64 | 10.10.4.128/25      
C | 50 | 12 | 10.10.5.0/26        

Total available addresses: 2048
Allocated blocks: [4, 4, 4, 2, 2, 2, 2, 1]
Block size: 64
Offset: [0, 4, 8, 12, 14, 16, 18, 20]
Legend: (#) Allocated block, (-) Free block
\#####################-----------
