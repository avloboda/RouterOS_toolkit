# This module can definitely be clean up a bit more. It was first written with the intention to 
# check every setting needed for remote logging functionality. I then found out that RouterOS will
# not allow you to edit an individual settings for an existing logging configuration through the API
# It will allow you to either create a new logging configuration set, or delete an existing one.

# This module will check if a configuration currently exists with your desired configuration name,
# if it exist, it will not do anything. If it does not exist it will add it.
# Do not use this module to change your logging settings from one server to another. You will end up
# with two syslog configurations on each of your devices. If you need to change your logging from one 
# server to another, I would recommend running a separate script to remove the existing configuration.

import desiredState
from modules import counters

def syslog(api, currentDate):
    parms = {
    'name':desiredState.syslogServerName, 'target':desiredState.syslogTarget,
    'remote':desiredState.syslogIPaddress, 'bsd-syslog':desiredState.syslogBSDformat
    }
    iteration = 0 # track which item contains the settings if they are present.
    existingID = None
    try:
        output = api(cmd='/system/logging/action/print')
        for item in output:                    # this loop establishes if desired destination exists.
            checkName = item['name']
            iteration += 1
            if checkName == desiredState.syslogServerName:
                existingID = item['.id'] # this variable is set for condition testing purposes
                iteration -= 1 # adjust due to zero start
                break

        if existingID == None: # if desired destination does not exist, 
            api(cmd='/system/logging/action/add', **parms)
            api(cmd='/system/logging/add', action=desiredState.syslogServerName, topics='critical')
            api(cmd='/system/logging/add', action=desiredState.syslogServerName, topics='error')
            api(cmd='/system/logging/add', action=desiredState.syslogServerName, topics='warning')
            api(cmd='/system/logging/add', action=desiredState.syslogServerName, topics='info')
            counters.syslogCorrections += 1
            with open('log-{}.txt'.format(currentDate), 'a') as file:
                file.write('Added all syslog settings.\n')
        else:
            with open('log-{}.txt'.format(currentDate), 'a') as file:
                file.write('No changes to syslog settings \n')

    except Exception as unknown_error:
        with open('log-{}.txt'.format(currentDate), 'a') as file:
            file.write('Error has occured: {}\n'.format(unknown_error))