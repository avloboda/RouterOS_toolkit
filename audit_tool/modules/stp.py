import desiredState
from modules import counters

def check_stp(api, current_date):
    try:
        output = api(cmd='/interface/bridge/print')
        
        parms = {'protocol-mode': desiredState.stpMode}

        if output[0]['protocol-mode'] != desiredState.stpMode:
            api(cmd='/interface/bridge/set', numbers=0, **parms)
            with open('log-{}.txt'.format(current_date), 'a') as file:
                file.write('Set STP state to: {}\n'.format(desiredState.stpMode))
            counters.stpCorrections += 1
        else:
            with open('log-{}.txt'.format(current_date), 'a') as file:
                file.write('No changes to STP state.\n')

    except Exception as unknown_error:
        with open('log-{}.txt'.format(current_date), 'a') as file:
            file.write('Error has occured: {}\n'.format(unknown_error))