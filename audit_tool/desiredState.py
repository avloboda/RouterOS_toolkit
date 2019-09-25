# Warning: If you would like to turn off a module, set all the variables for that module to None, 
# or, turn off the module entirely by commenting out the function call in the "run.py" file.

ntpStatus = True # "True" for NTP enabled, "False" for NTP disabled.
ntpServer = '10.10.1.1' # set the desired NTP server IP address.
stpMode = 'rstp' # turn on RSTP
snmpStatus = True # enable SNMP, True or False
snmpCommunity = 'secretString' # set the community string.