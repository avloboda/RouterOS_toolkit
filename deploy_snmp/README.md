# Mikrotik SNMP Deployment

I recommend using the audit tool that is in the parent directory to deploy and enforce SNMP settings.

This script establishes an API connection with a device and configures SNMPv2c settings. A "devices_list" file must exist in the same directory as the script and contain the IPs or hostnames of the devices to be configured, one per line.

Edit your configuration in the runcode() function.

### Requirements 
*Requires Python3.6+
*Requires Librouteros 2.2.0 library, which can be found here: https://github.com/luqasz/librouteros