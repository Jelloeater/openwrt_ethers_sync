# /// script
# requires-python = ">=3.7"
# dependencies = [
#   "paramiko",
# ]
# ///

# Install UV for above deps
# wget -qO- https://astral.sh/uv/install.sh | sh


#Globals
SCRATCH_FILE='./openwrt_ethers'

import logging
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)8s] %(message)s (%(filename)s:%(funcName)s():%(lineno)s)",
    level=logging.INFO,
)

import re,os


def convert_leases_to_ethers():
    ethers_entries = []
    
    with open('/var/lib/dhcp/dhcpd.leases', 'r') as leases_file:
        leases_content = leases_file.read()
        
    lease_blocks = re.findall(r'lease .+? {(.+?)}', leases_content, re.DOTALL)
    
    for block in lease_blocks:
        mac = re.search(r'hardware ethernet (.+?);', block)
        hostname = re.search(r'client-hostname "(.+?)";', block)
        
        if mac and hostname:
            ethers_entries.append(f"{mac.group(1)} {hostname.group(1)}")
    
    with open(SCRATCH_FILE, 'w') as ethers_file:
        ethers_file.write('\n'.join(ethers_entries))

convert_leases_to_ethers()

import paramiko
 
with paramiko.SSHClient() as ssh:
    ssh.load_system_host_keys()
    ssh.connect('uap', username='root')
 
    sftp = ssh.open_sftp()

    sftp.put(SCRATCH_FILE, '/etc/ethers')
os.remove(SCRATCH_FILE)
