#!.env/bin/python

import pexpect
import re

# at least we need mapping: NIC name (ethX) - mac address - switch - port
# ethX is key in dictionary

# Host names

fuel = 'fuel-dc209'
swa = 'dc209-swa'
swb = 'dc209-swb'

password = ''
#swb = 'dc157-swb'

# NICs

eth_list = ['eth0','eth1','eth2','eth3']


swa_command = 'ssh ' + swa + ' \'show ports info\''
swb_command = 'ssh ' + swb + ' \'show ports info\''
fuel_command = 'ssh ' + fuel + ' fuel nodes --env 1'

def exec_cmd(cmd):
    ssh_newkey = 'Are you sure you want to continue connecting'
    # my ssh command line
    p=pexpect.spawn(cmd)
    i=p.expect([ssh_newkey,'Enter password for admin:',pexpect.EOF])
    if i==0:
	print "I say yes\n"
	p.sendline('yes')
	i=p.expect([ssh_newkey,'Enter password for admin:',pexpect.EOF])
    if i==1:
	print "I give password\n",
	p.sendline(password)
	p.expect(pexpect.EOF)
    elif i==2:
	print "I either got key or connection timeout\n"
	pass
    print cmd
    print p.before # print out the result
    return p.before

# Before call this func ensure:
# corresponding NIC on the node is connected to the switch
# this NIC doesn't look into PXE network
# it is in UP state
#
def find_port(ip,iface):
    # Prepare command to set NIC 'UP'
    ifup = 'ssh ' + fuel + ' ssh ' +  ip + ' ifconfig ' + iface + ' up'
    # Execute command
    exec_cmd(ifup)
    # in furure - check if link ok at this point
    # verify_link()
    # Get port maps for both switches when link is UP
    swa_portmap1 = get_portmap(swa_command,'up')
    swb_portmap1 = get_portmap(swb_command,'up')
    # Prepare command to 'DOWN' the link
    ifdown = 'ssh ' + fuel + ' ssh ' +  ip + ' ifconfig ' + iface + ' down'
    # execute command
    exec_cmd(ifdown)
    # Get portmap for both switches when link is DOWN
    swa_portmap2 = get_portmap(swa_command,'down')
    swb_portmap2 = get_portmap(swb_command,'down')
    # Set link UP
    exec_cmd(ifup)
    # Get comparation dictionary
    for key in swa_portmap1:
	if swa_portmap2[key] != swa_portmap1[key]:
	    port = key
	    sw = 'swa'
    for key in swb_portmap1:
	if swb_portmap2[key] != swb_portmap1[key]:
	    port = key
	    sw = 'swb'
    #return [swa_portmap1,swb_portmap1]
    #should be:
    #return ['switch_name','port_number']
    return [sw,port]

def get_portmap(sw_command, link_status):
    portmap = {}
    lines = re.split('\n',exec_cmd(sw_command))
    # Get the dictionary of active ports (rest of them aren't needed)
    for line in lines:
	# I'm not sure it is the best regexp to use in this case
        if re.search('Em-.*', line):
	    ln = line.split( );
	    if link_status == 'up':
		if ln[2] == 'active':
		    portmap[ln[0]] = ln[2]
	    else:
		portmap[ln[0]] = ln[2]
    return portmap

def get_nodes_list():
    nodes_list={}
    nodes = re.split('\n',exec_cmd(fuel_command))
    for node in nodes:
	if re.search('True.*',node):
	    nd = node.split( );
	    nodes_list[nd[0]] = [nd[2],nd[9]]
    return nodes_list

def get_port_mapping():
    port_mapping = {}
    n_list = get_nodes_list()
    for key in n_list:
	eth_dict = {}
	for e in eth_list:
	    cmd = 'ssh ' + fuel + ' ssh ' +  n_list[key][1] + ' ifconfig ' + e + ' | grep Ethernet'
	    ifc = exec_cmd(cmd)
	    eth = ifc.split( );
	    # Get switch name and switch port (list)
#	    sw_port = find_port(n_list[key][1],eth[11])
	    sw_port = find_port(n_list[key][1],e)
	    eth_dict[e] = [eth[15],sw_port[0],sw_port[1]]
	port_mapping[n_list[key][1]] = eth_dict
    return port_mapping


mapping = get_port_mapping()
for key in mapping:
    print ' '
    print key
    eth_map = mapping[key]
    for key in eth_map:
	print key +' - ' + eth_map[key][0] +' - ' + eth_map[key][1] +' - ' + eth_map[key][2]

