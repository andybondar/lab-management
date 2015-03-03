#!.env/bin/python

from fabric.api import run, env

# Host names

user = 'admin'

swa = 'host1'
swb = 'host2'

swa_url = user + '@' + swa
swb_url = user + '@' + swb

print swa_url
print swb_url

#env.hosts = [swa_url, swb_url]
#env.passwords = {swa_url: '', swb_url: ''}

#run('show version')



