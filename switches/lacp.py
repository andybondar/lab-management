#!.env/bin/python

import pexpect

# Host names
swa = 'dc192-swa'
swb = 'dc192-swb'
user = 'admin'
password = ''

# Ports
portlist = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,55]


def enable_lacp():
    for n in portlist:
	enable_mlag_swa = 'ssh ' + user + '@' + swa + ' \'enable mlag port ' + `n` + ' peer \"EXTREME1\" id ' + `n` + '\''
	enable_mlag_swb = 'ssh ' + user + '@' + swb + ' \'enable mlag port ' + `n` + ' peer \"EXTREME1\" id ' + `n` + '\''

	if n == 49:
	    enable_sharing_swa = 'ssh ' + user + '@' + swa + ' \'enable sharing ' + `n` + ' grouping 49-52 algorithm address-based L2 lacp\''
	    enable_sharing_swb = 'ssh ' + user + '@' + swb + ' \'enable sharing ' + `n` + ' grouping 49-52 algorithm address-based L2 lacp\''
	else:
	    enable_sharing_swa = 'ssh ' + user + '@' + swa + ' \'enable sharing ' + `n` + ' grouping '+ `n`  +' algorithm address-based L2 lacp\''
	    enable_sharing_swb = 'ssh ' + user + '@' + swb + ' \'enable sharing ' + `n` + ' grouping '+ `n`  +' algorithm address-based L2 lacp\''

	exec_cmd(enable_sharing_swa)
	exec_cmd(enable_mlag_swa)
	exec_cmd(enable_sharing_swb)
	exec_cmd(enable_mlag_swb)

    return


def disable_lacp():
    for n in portlist:
	disable_mlag_swa = 'ssh ' + user + '@' + swa + ' \'disable mlag port ' + `n` + '\''
	disable_mlag_swb = 'ssh ' + user + '@' + swb + ' \'disable mlag port ' + `n` + '\''
	disable_sharing_swa = 'ssh ' + user + '@' + swa + ' \'disable sharing ' + `n` + '\''
	disable_sharing_swb = 'ssh ' + user + '@' + swb + ' \'disable sharing ' + `n` + '\''

	exec_cmd(disable_mlag_swa)
	exec_cmd(disable_sharing_swa)
	exec_cmd(disable_mlag_swb)
	exec_cmd(disable_sharing_swb)

    return


def exec_cmd(cmd):
#    print cmd
#    command = 'ssh ' + swa + ' show fdb | inc 82:ca:3d:6b:a2:4a'

    ssh_newkey = 'Are you sure you want to continue connecting'
    # my ssh command line
    p=pexpect.spawn(cmd)
    i=p.expect([ssh_newkey,'Enter password for admin:',pexpect.EOF])
    if i==0:
	print "I say yes"
	p.sendline('yes')
	i=p.expect([ssh_newkey,'Enter password for admin:',pexpect.EOF])
    if i==1:
	print "I give password",
	p.sendline(password)
	p.expect(pexpect.EOF)
    elif i==2:
	print "I either got key or connection timeout"
	pass
    print p.before # print out the result
    return


###############

import sys

#action = sys.argv[1]

if len(sys.argv) < 2:
    print 'Usage: ./lacp {enable|disable}'
    sys.exit(1)

if sys.argv[1] == 'enable':
    enable_lacp()
elif sys.argv[1] == 'disable':
    disable_lacp()
else:
    print 'Usage: ./lacp {enable|disable}'
