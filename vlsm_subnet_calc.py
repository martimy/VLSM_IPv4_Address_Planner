"""
Examples of usage
"""

from address_planner_4 import AddressPlan4

if __name__ == '__main__':
    network = '192.168.64.0/19'
    req_subnets = {'A': 1777, 'B': 1560, 'C': 500,
                   'D': 672, 'E': 123, 'F': 904, 'G': 677, 'H': 67}
    plan = AddressPlan4(req_subnets)
    result = plan.plan(network)
    print(result.get_output())
    print(plan.get_map())

    network = '10.10.0.0/21'
    req_subnets = {'A': 177, 'B': 160, 'C': 50,
                   'D': 62, 'E': 123, 'F': 104, 'G': 67, 'H': 67}
    plan = AddressPlan4(req_subnets)
    #plan.plan_old(network, req_subnets)
    result = plan.plan(network)
    print(result.get_output())
    print(plan.get_map())

    network = '192.168.32.0/19'
    req_subnets = {'Operations1': 2150, 'Operations2': 975,
                   'Operations3': 175, 'Sales': 575, 'DMZ': 5}
    plan = AddressPlan4(req_subnets, scale=1.0)
    #plan.plan_old(network, req_subnets)
    result = plan.plan(network)
    print(result.get_output())
    # print('Allocated = {:0.1f}'.format(alloc))
    print(plan.get_map())

    network = '192.168.0.0/18'
    req_subnets = {'B1_Legal': 120, 'B1_Acc': 370, 'B1_DMZ': 5, 'B2_HQ': 1580,
                   'B2_Eng': 200, 'B2_DMZ': 5, 'B3_Operations1': 2150,
                   'B3_Operations2': 975, 'B3_Operations3': 175,
                   'B3_Sales': 575, 'B3_DMZ': 5, 'B4_Sales': 75,
                   'B4_Market': 75, 'B4_DMZ': 5, 'B5_Sales': 80, 'P2P': 10}
    plan = AddressPlan4(req_subnets, scale=1.0)
    result = plan.plan(network)
    print(result.get_output())
    # print('Allocated = {:0.1f}'.format(alloc))
    print(plan.get_map())

    network = '192.168.128.0/20'
    req_subnets = {'B1': 200, 'B2': 200,
                   'L1': 2, 'L2': 2,
                   'DMZ': 15, 'H1': 200, 'DC': 100}
    plan = AddressPlan4(req_subnets, scale=1.2)
    result = plan.plan(network, method="FIRST")
    print(result.get_output())
    # print('Allocated = {:0.1f}'.format(alloc))
    print(plan.get_map())
