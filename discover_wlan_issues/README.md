# Discover Potential PtP Issues

This script collects wireless data from each device and formats it into a CSV file. 
Up to two files will be created. One will be a complete list of all registered PtP connections and one will contain connections that break your configured parameters. 

Data collected for each device:
- tx signal strength (ch0/ch1)
- Signal-to-noise ratio
- Link ID
- Frequency
- Channel-width

Conditions data is tested against:
- Low signal strength
- Lopsided signals
- Low signal-to-noise ratio

Edit the variables in the "main.py" file to suit your tolerances. The current settings are there with the QRT 5 ac in mind.

### Requirements 
* Requires Python3.6+
* Requires Librouteros 2.2.0+ library, which can be found here: https://github.com/luqasz/librouteros