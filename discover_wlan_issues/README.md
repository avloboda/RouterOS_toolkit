# Discover Potential PtP Issues

This script collects data from each device and formats it to be imported into Excel. 
Up to two files will be created. One will be a complete list of all registered PtP connections and one will contain connections that break your configured parameters. 

Data collected for each device:
- tx signal strength (ch0/ch1)
- Signal-to-noise ratio
- Link ID

Conditions data is tested against:
- Low signal strength
- Lopsided signals
- Low signal-to-noise ratio

Tested with Python3.6

Scripts require the librouteros 2.2.0+ library, which can be found here: https://github.com/luqasz/librouteros