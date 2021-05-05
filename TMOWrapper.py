import subprocess

class TMOWrapper:
	"""
    This Wrapper will be used to call takemeon to check for dangling subdomains pointing to nxdomain
    Define function to check for nxdomain domain and output true or false for each domain indicating whether they are dangling subdomains pointing to nxdomains
    """

	"""
	As a first step, we will see if takemeon is installed or not, if not, we will exit the program with appropriate error
	"""
	def __init__(self):
		status = subprocess.getstatusoutput('takemeon')[0]
		if(status != 0):
			print("Error: takemeon not found on the system")
			exit(1)

	"""
	We expect input of following format.
	[{'sub':'test.example.com','resolution':''}, {'sub':'test2.example.com','resolution':''}, ...]
	Output:
	[{'sub':'test.example.com','resolution':'', 'tko':false}, {'sub':'test2.example.com','resolution':'', 'tko', true}, ... ]
	"""	
	def check_takeover(self, subdomain_list):
		#print(subdomain_list)
		subdomain_string = ''
		for i in subdomain_list:
			subdomain_string += i['sub']
			subdomain_string += "\n"
		p = subprocess.Popen(['takemeon','-json-output','-mdns', '8.8.8.8'], stdin=subprocess.PIPE)
		try:
			p.stdin.write(str.encode(subdomain_string))
		except IOError as e:
			if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
				# Stop loop on "Invalid pipe" or "Invalid argument".
				# No sense in continuing with broken pipe.
				print("Error: invalid input received")
				exit(1)
			else:
				# Raise any other error.
				raise

		p.stdin.close()
		p.wait()

			




t = TMOWrapper()
test_domains = [{'sub':'takeover4.xve.io','res':'totallynonexistingdomain2.com'}, {'sub':'takeover5.xve.io', 'res':'takeover4.xve.io'}]
t.check_takeover(test_domains)