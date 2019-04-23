#!/usr/bin/env python3.6
from librouteros.login import login_plain
from librouteros import connect, ConnectionError
import getpass, time
# This script establishes an API connection with a device and configures remote logging settings.
# A "devices_list" file must exist in the same directory as the script and contain the IPs or hostnames
# of the devices to be configured, one per line.

method = (login_plain,) # using the plaintext API, not recommended for use across WAN.

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

start_time = time.time()

with open('devices_list') as file:    # Opens, reads, and preps the IPs/hostnames of the devices to be configured. 
	devices_list = file.read().splitlines()

for device in devices_list:    # Main logic loop. Connects, and deploys configuration.
	print('Connecting to {}'.format(device))
	api = login(username, password, device)    # establish a connection
	# Librouteros does not raise an exception if the credentials are incorrect. It sets the connection variable to None instead.
	# The below line checks if a connection really has been established, if not, tries next device.
	if api == None:
		print('Failed to establish a connection. Moving on to next device.')
		print('----------------------------------------------------')
		continue

	print('Configuring {}'.format(device))
	parms = {'name':'syslog', 'target':'remote', 'remote':'10.2.2.2', 'bsd-syslog':True}
	try:
		api(cmd='/system/logging/action/add', **parms)
		api(cmd='/system/logging/add', action='syslog', topics='critical')
		api(cmd='/system/logging/add', action='syslog', topics='error')
		api(cmd='/system/logging/add', action='syslog', topics='warning')
		api(cmd='/system/logging/add', action='syslog', topics='info')
	except Exception as unknown_error:
		print('Error has occured: {}'.format(unknown_error))
		continue
		
	api.close()
	print('----------------------------------')

total_runtime = time.time() - start_time
print('Total runtime {}'.format(total_runtime))