#!/usr/bin/env python3.6
from librouteros.login import login_plain
from librouteros import connect, ConnectionError
import time, getpass
# See README.md for information
# https://github.com/avloboda
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
        
def runcode(command):    # this function makes API calls to the device.
    try:
        output = api(cmd=command)
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
    
    print('Retrieving data...')
    output = runcode('/system/resource/print')
    board_name = output[0]['board-name']
    architecture = output[0]['architecture-name']
    output = runcode('/system/routerboard/print')
    version = output[0]['current-firmware']
    output = runcode('/system/identity/print')
    hostname = output[0]['name']

    try:
        print('Writing to complete-list file...')
        with open('complete_list-{}.csv'.format(current_date), 'a') as file:
            file.write('{},{},{},{},{}\n'.format(device,hostname,board_name,architecture,version))
    except Exception as unknown_error:
        print(unknown_error)

    if architecture == 'arm':
        try:
            print('Writing to arm file...')
            with open('arm_devices_list-{}.csv'.format(current_date), 'a') as file:
                file.write('{},{},{},{},{}\n'.format(device,hostname,board_name,architecture,version))
        except Exception as unknown_error:
            print(unknown_error)

    if architecture == 'mipsbe':
        try:
            print('Writing to mipsbe device file...')
            with open('mipsbe_devices_list-{}.csv'.format(current_date), 'a') as file:
                file.write('{},{},{},{},{}\n'.format(device,hostname,board_name,architecture,version))
        except Exception as unknown_error:
            print(unknown_error)

    if architecture == 'tile':
        try:
            print('Writing to tile device file...')
            with open('tile_devices_list-{}.csv'.format(current_date), 'a') as file:
                file.write('{},{},{},{},{}\n'.format(device,hostname,board_name,architecture,version))
        except Exception as unknown_error:
            print(unknown_error)    

    print('----------------------------------------------------')
    api.close()

total_runtime = time.time() - start_time    # collect total runtime.
print('Total runtime {}'.format(total_runtime))