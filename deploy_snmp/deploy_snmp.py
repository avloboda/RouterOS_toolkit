#!/usr/bin/env python3.6
from librouteros.login import login_plain
from librouteros import connect, ConnectionError
import getpass, time

method = (login_plain,) # using the plaintext API

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
		
def runcode():    # this is where the script will send API calls to the device.
	parms = {'enabled':True, 'contact':'', 'trap-target':'192.168.2.1', 'trap-community':'communityname', 'trap-version':'2'}
	try:
		api(cmd='/snmp/community/add', name='communityname')
	except Exception as unknown_error:
		print('Error has occured: {}'.format(unknown_error))
	try:
		api(cmd='/snmp/set', **parms)
		return 'Configuration pushed successfully'
	except Exception as unknown_error:
		print('Error has occured: {}'.format(unknown_error))
		return unknown_error

start_time = time.time()    # times the script.

with open('devices_list') as file:    # this block reads the list of devices (hostnames or IPs) to be configured
	devices_list = file.read().splitlines()

for device in devices_list:    # Main logic loop. Connects and deploys configuration.
	print('Connecting to {}'.format(device))
	api = login(username, password, device)    # establish a connection
	# Librouteros does not raise an exception if the credentials are incorrect. It sets the connection variable to None instead.
	# The below line checks if a connection really has been established, if not, moves on to next device.
	if api == None:
		print('Failed to establish a connection. Moving on to next device.')
		print('----------------------------------------------------')
		continue
	
	results = runcode()
	print(results)
	print('-------------------------------')
	api.close()

total_runtime = time.time() - start_time    # collect total time.
print('Total runtime {}'.format(total_runtime))