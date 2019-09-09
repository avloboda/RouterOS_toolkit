# Warning: If you would like to turn off a module, set all the variables for that module to None. I do not recommend 
# turning off modules, instead, just set the desired state and enforce it throughout the network. 

ntpStatus = True # "True" for NTP enabled, "False" for NTP disabled.
ntpServer = '10.10.1.1' # set the desired NTP server IP address.
stpMode = 'rstp' # turn on RSTP