# Mikrotik Audit Tool

The purpose of this tool is to enforce network specific configurations on Mikrotik wireless radios. The "desiredState.py" file contains variables to be enforced. 

Currently supports enforcing:
* NTP settings (status and server)
* STP mode (mode only, priorities should be optimized manually)
* SNMP settings (status and community string)
* Syslog settings (remote server logging)

To turn off a module, comment out the function call for the module in the "run.py" file.

### Logging enforcement limitation

Due to a RouterOS API limitation, you cannot edit a logging configuration set once it is on the device. Do not use the syslog module to edit an existing configuration. This module will check if a configuration currently exists with your desired configuration name, if it exist, it will not do anything. If it does not exist, it will add it. Do not use this module to change your logging settings from one server to another. You will end up with two syslog configurations on each of your devices. If you need to change your logging from one server to another, I would recommend running a separate script to remove the existing configuration, then running this one to push the new one.


Please report any bugs.

### Requirements
* Requires Python 3.6+.
* Requires Librouteros 2.2.0+ library, which can be found here: https://github.com/luqasz/librouteros
