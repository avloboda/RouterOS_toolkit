#!/usr/bin/env python3
from librouteros.login import login_plain
from librouteros import connect, ConnectionError
import time, getpass
import desiredState 
from lib import ntp
# https://github.com/avloboda
# See README.md for information

method = (login_plain,) # using the plaintext API
current_date = time.strftime('%m-%d-%Y') # get todays date; will be appended to log file name.

def login(username, password, device):
	try:
		api = connect(username=username, password=password, host=device, login_methods=method)
		return api
	except ConnectionError:
		print('Connection has either been refused, or the host is unreachable. Check if API is exposed on device.')
		with open('log-{}.txt'.format(current_date), 'a') as file:
			file.write('Error has occured: {}'.format(unknown_error))
		return None
	except Exception as unknown_error:
		print('Error has occured: {}'.format(unknown_error))
		with open('log-{}.txt'.format(current_date), 'a') as file:
			file.write('Error has occured: {}'.format(unknown_error))
		return None

username = input('Enter your username: ')
password = getpass.getpass(prompt='Enter your password: ', stream=None)

print('----------------------------------')

start_time = time.time()

with open('devices_list') as file:    # this block reads the list of devices (hostnames or IPs) to be configured
	devices_list = file.read().splitlines()

for device in devices_list:
	print('Connecting to {}'.format(device))
	api = login(username, password, device)    # establish a connection
	# Librouteros does not raise an exception if the credentials are incorrect. It sets the connection variable to None instead.
	# The below line checks if a connection really has been established, if not, tries next device.
	if api == None:
		with open('log-{}.txt'.format(current_date), 'a') as file:
			file.write('Failed to establish a connection to {}\n'.format(device))
			file.write('--------------------------------------\n')
		print('Failed to establish a connection. Moving on to next device.')
		print('----------------------------------------------------')
		continue

	with open('log-{}.txt'.format(current_date), 'a') as file:
			file.write('Connected to {}\n'.format(device))

	ntp.check_ntp(api, current_date)
	api.close()
	with open('log-{}.txt'.format(current_date), 'a') as file:
		file.write('-------------------------------------------\n')
	print('----------------------------------')

print('End of device list')

with open('log-{}.txt'.format(current_date), 'a') as file:
	file.write('End of device list\n')
	file.write('-------------------------------------------\n')

total_runtime = time.time() - start_time
print('Total runtime {}'.format(total_runtime))