import desiredState
from modules import counters

def check_snmp(api, currentDate):
    stringExists = 0
    try:
        output = api(cmd='/snmp/community/print')

        for i in range(len(output)): # check if community string exists on device
            if output[i]['name'] == desiredState.snmpCommunity:
                stringExists += 1
        
        if stringExists == 0: # set the community string if it does not exist.
            api(cmd='/snmp/community/add', name=desiredState.snmpCommunity)
            with open('log-{}.txt'.format(currentDate), 'a') as file:
                file.write('Added SNMP community: {}\n'.format(desiredState.snmpCommunity))
            counters.snmpCorrections += 1
        else:
            with open('log-{}.txt'.format(currentDate), 'a') as file:
                file.write('No changes to SNMP community state.\n')

        parms = {'enabled': desiredState.snmpStatus}
        output = api(cmd='/snmp/print')

        if output[0]['enabled'] != desiredState.snmpStatus:
            api(cmd='/snmp/set', **parms)
            with open('log-{}.txt'.format(currentDate), 'a') as file:
                file.write('Set SNMP enable status to: {}\n'.format(desiredState.snmpStatus))
            counters.snmpCorrections += 1
        else:
            with open('log-{}.txt'.format(currentDate), 'a') as file:
                file.write('No changes to SNMP enable status.\n')

    except Exception as unknown_error:
        with open('log-{}.txt'.format(currentDate), 'a') as file:
            file.write('Error has occured: {}\n'.format(unknown_error))