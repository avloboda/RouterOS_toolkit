# Mikrotik Syslog Deployment

Tested with Python3.6

Requires librouteros 2.2.0 library, which can be found here: https://github.com/luqasz/librouteros

This script establishes an API connection with a device and configures remote logging settings. A "devices_list" file must exist in the same directory as the script and contain the IPs or hostnames of the devices to be configured, one per line.
