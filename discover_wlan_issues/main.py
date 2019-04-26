#!/usr/bin/env python3.6
from librouteros.login import login_plain
from librouteros import connect, ConnectionError
import time, getpass
# See README.md for information
method = (login_plain,) # using the plaintext API
current_date = time.strftime('%m-%d-%Y') # get todays date; will be appended to config filenames.

username = input('Enter your username: ')
password = getpass.getpass(prompt='Enter your password: ', stream=None)
print('----------------------------------')

signalthreshold = -75 # wireless signal threshold
lopsidedthreshold = 6 # the two channels should be identical under good conditions
snrthreshold = 15 # SNR threshold

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
		
def runcode(command, extra):    # this is where the script will sends API calls to the device.
	try:
		output = api(cmd=command, stats=extra)
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

	output = runcode('/interface/wireless/registration-table/print', True)
	
	if output == (): # check if anything was returned (if interface is disabled, empty tuple returned.)
		print('Wlan interface is likely disabled/no connected clients/or a 60G interface. Moving on to next device.')
		continue
	elif 'tx-signal-strength-ch0' not in output[0]: #known issues, if persists, consider running the runcode function twice
		print('Device did not return tx-signal-strength. Moving on to next device.')
		continue

	for i in range(len(output)):	# making another loop here in case there are multiple connections at this AP.
		wlanid = output[i]['.id']
		ch0 = int(output[i]['tx-signal-strength-ch0'])
		ch1 = int(output[i]['tx-signal-strength-ch1'])
		snr = int(output[i]['signal-to-noise'])
		issues = 0 # keep track of potential problems
		difference = abs(ch0-ch1) # get the difference in signals

		if ch0 < signalthreshold or ch1 < signalthreshold:
			issues += 1
		elif difference >= lopsidedthreshold:
			issues += 1
		elif snr <= snrthreshold:
			issues += 1

		if issues >= 1:
			try:
				print('Found potential issue...')
				with open('potential_issues-{}.txt'.format(current_date), 'a') as file:
					file.write('{}\t{}\t{}\t{}\t{}\n'.format(device,ch0,ch1,wlanid,snr))
			except Exception as unknown_error:
				print(unknown_error)

		try:
			print('Writing to file...')
			with open('complete_wlan_list-{}.txt'.format(current_date), 'a') as file: # create a file and write the results
				file.write('{}\t{}\t{}\t{}\t{}\n'.format(device,ch0,ch1,wlanid,snr))
		except Exception as unknown_error:
			print(unknown_error)

	print('----------------------------------------------------')
	api.close()

total_runtime = time.time() - start_time    # collect total time.
print('Total runtime {}'.format(total_runtime))