# Mikrotik Audit Tool - WIP

The purpose of this tool is to enforce network specific configurations on Mikrotik wireless radios. The "desiredState.py" file contains variables to be enforced. 

Currently supports enforcing:
* NTP settings (status and server)
* STP mode (mode only, priorities should be optimized manually)
* SNMP settings (status and community string)

Requires Python 3.6+.

Requires librouteros 2.2.0+ library, which can be found here: https://github.com/luqasz/librouteros