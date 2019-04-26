# Document Devices

This script collects data from each device and formats it to be imported into Excel. 
Depending on your network, up to four files will be created by default. At least one is always created. The first file is a complete list with information on all the devices. The other files are created based on the architecture of the device. Currently, the script is configured to create separate files for devices for each of the following: ARM, MIPSBE, and TILE architectures.

Data collected for each device:
- IP address
- Hostname
- Device model
- Architecture
- Running firmware version

Tested with Python3.6

Scripts require the librouteros 2.2.0+ library, which can be found here: https://github.com/luqasz/librouteros