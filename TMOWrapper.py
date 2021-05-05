import subprocess
import json

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
	[{'domain':'test.example.com','resolution':'test1.com', 'tko':true}, {'domain':'test2.example.com','resolution':'', 'tko', true}, ... ]
	"""	
	def check_takeover(self, subdomain_list):
		subdomain_string = ''
		for i in subdomain_list:
			subdomain_string += i['sub']
			subdomain_string += "\n"
		try:
			p = subprocess.Popen(['takemeon','-json-output','-mdns', '8.8.8.8'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			output, error = p.communicate(str.encode(subdomain_string))
			if output == b'null\n':
				return []
			output_string = output.decode("utf-8")
			output_json = json.loads(output_string)
			for i in output_json:
				i['tko'] = True
			# print(output_json)
			return output_json
			
		except FileNotFoundError as e:
			print("Unable to locate takemeon during execution")
		except IOError as e:
			if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
				# Stop loop on "Invalid pipe" or "Invalid argument".
				# No sense in continuing with broken pipe.
				print("Error: invalid input received")
				exit(1)
			else:
				# Raise any other error.
				raise



			



# Example Usage:
t = TMOWrapper()
test_domains2 = [{'sub':'test.google.com'}]
test_domains = [{'sub':'takeover4.xve.io','res':'totallynonexistingdomain2.com'}, {'sub':'takeover5.xve.io', 'res':'takeover4.xve.io'}, {'sub':'takeover1.xve.io', 'res':''}]
result = t.check_takeover(test_domains2)
if len(result) != 0:
	print(result)
else:
	print("[!] No SDTKO through takemeon")

# Output:
"""
For test_domains: [{'domain': 'takeover4.xve.io', 'resolution': 'totallynonexistingdomain2.com', 'tko': True}, {'domain': 'takeover5.xve.io', 'resolution': 'takeover4.xve.io', 'tko': True}]
FOr test_domains2: []
"""