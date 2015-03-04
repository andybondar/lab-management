#!.env/bin/python

import pexpect
import re


# Host names

fuel = 'fuel-dc209'
swa = 'dc209-swa'
swb = 'dc209-swb'

password = ''
#swb = 'dc157-swb'


#arr[]

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
def find_port():
    swa_portmap1 = get_first_portmap(swa_command)
    swb_portmap1 = get_first_portmap(swb_command)
    return [swa_portmap1,swb_portmap1]

def get_first_portmap(sw_command):
    portmap = {}
    lines = re.split('\n',exec_cmd(sw_command))
    # Get the dictionary of active ports (rest of them aren't needed)
    for line in lines:
	# I'm not sure it is the best regexp to use in this case
        if re.search('Em-.*', line):
	    ln = line.split( );
	    if ln[2] == 'active':
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

#print find_port()
list = get_nodes_list()
print list['1'][1]