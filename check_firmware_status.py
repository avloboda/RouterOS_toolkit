#!/usr/bin/env python3.6
from librouteros.login import login_plain
from librouteros import connect, ConnectionError
import time, getpass
# https://github.com/avloboda
# This script connects to each device via API and retrieves firmware versions.
# The running and available versions get written to a file. You can format the output according to your needs.

method = (login_plain,) # using the plaintext API
current_date = time.strftime('%m-%d-%Y') # get todays date; will be appended to config filenames.

username = input('Enter your username: ')
password = getpass.getpass(prompt='Enter your password: ', stream=None)
print('----------------------------------')

def login(username, password, device):
    try:
        api = connect(username=username, password=password, host=device, login_methods=method)
        return api
    except ConnectionError:
        print('Connection has either been refused, or the host is unreachable. Check if API is exposed on device.')
        return None
    except Exception as unknown_error:
        print('Error has occured: {}'.format(unknown_error))
        return None
        
def runcode():    # this is where the script will sends API calls to the device.
    try:
        output = api(cmd='/system/routerboard/print')
        return output
    except Exception as unknown_error:
        print('Error has occured: {}'.format(unknown_error))
        return unknown_error

start_time = time.time()    # times the script.

with open('devices_list') as file:    # this block reads the list of devices (hostnames or IPs) to be configured
    devices_list = file.read().splitlines()

for device in devices_list:
    print('Connecting to {}'.format(device))
    api = login(username, password, device)    # establish a connection
    # Librouteros does not raise an exception if the credentials are incorrect. It sets the connection variable to None instead.
    # The below line checks if a connection really has been established, if not, tries next device.
    if api == None:
        print('Failed to establish a connection. Moving on to next device.')
        print('----------------------------------------------------')
        continue

    print('Retrieving output...')
    output = runcode()
    current_fw = output[0]['current-firmware']
    available_fw = output[0]['upgrade-firmware']

    try:
        print('Writing to file...')
        with open('firmware-{}.txt'.format(current_date), 'a') as file: # create a file and write the results
            file.write('----------------------------- {} -----------------------------'.format(device))
            if current_fw != available_fw:
                file.write('\nUPGRADE AVAILABLE')
            file.write('\nRunning firmware: {}'.format(current_fw))
            file.write('\nAvailable firmware: {}'.format(available_fw))
            file.write('\n------------------------------------------------------------------------\n\n\n')
    except Exception as unknown_error:
        print(unknown_error)

    print('----------------------------------------------------')
    api.close()

total_runtime = time.time() - start_time    # collect total time.
print('Total runtime {}'.format(total_runtime))