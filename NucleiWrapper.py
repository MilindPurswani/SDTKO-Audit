import subprocess
import os
import json 
class NucleiWrapper():
	"""
    This function will be used to check for Subdomain takeovers using Nuclei Scanner pointing to a 3rd party service
    Define a function that takes a list of dictionaries as input and returns true false for each subdomamin
    """

	"""
	Check if nuclie is installed. If installed call `nuclei -update-templates`
	"""
	def __init__(self):
		status = subprocess.getstatusoutput(['nuclei -version -silent'])[0]
		if(status != 0):
			print("[!] Error: nuclei not found on the system")
			exit(1)
		try:
			p = subprocess.Popen(['nuclei','-update-templates','-silent'])
			output, error = p.communicate()
		except FileNotFoundError:
			print("[!] Unable to update templates")


	# giving nuclei input from stdin. Perhaps not the best way to do this.	
	def input_to_nuclei(self, subdomain_list):
		subdomain_string = ''
		for i in subdomain_list:
			subdomain_string += "http://"+i['sub']
			subdomain_string += "\n"

		return subdomain_string

	# check for sdtko by running nuclei scanner
	def check_takeover(self, subdomain_list):
		#  stores a list of subdomains that are potentially vulnerable
		tko_list = []
		subdomain_string = self.input_to_nuclei(subdomain_list)
		try:
			# subprocess to call nuclei
			p = subprocess.Popen(['nuclei', '-t',os.path.expanduser("~/nuclei-templates/takeovers"),'-json','-silent'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			cmd_output, error = p.communicate(str.encode(subdomain_string))

			# check if nuclei output was null, if it was, return an empty list
			if cmd_output == b'null\n':
				return []
			# if output is present, then there is potential subdomain takeover	
			cmd_output_string = cmd_output.decode("utf-8")
			cmd_output_list = cmd_output_string.split("\n")
			cmd_output_list = cmd_output_list[:-1]
			# The output is in bytes, and contains multiple json strings, we need to loop through each string and parse the json.
			for i in cmd_output_list:
				d = {}
				cmd_output_element = json.loads(i)
				# removing the `http://` added in front to input_to_nuclei function to get the resolved domain from subdomain_list.
				d['sub'] = cmd_output_element['host'].replace('http://','')
				d['name'] = cmd_output_element['info']['name']
				d['tko'] = True
				for element in subdomain_list:
					if element['sub'] == d['sub']:
						d['resolution'] = element['resolution']
				tko_list.append(d)
			return tko_list
		except FileNotFoundError as e:
			print("[!] Unable to locate takemeon during execution")
		except IOError as e:
			if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
				# Stop loop on "Invalid pipe" or "Invalid argument".
				# No sense in continuing with broken pipe.
				print("[!] Error: invalid input received")
				exit(1)
			else:
				# Raise any other error.
				raise

# demo usage
n = NucleiWrapper()
test_domains2 = [{'sub':'test.google.com'}]
test_domains = [{'sub': '_domainconnect.xve.io', 'resolution': '_domainconnect.gd.domaincontrol.com'}, {'sub': 'mail.xve.io', 'resolution': 'domain.mail.yandex.net'}, {'sub': 'takeover1.xve.io', 'resolution': 'non-existing-domain.github.io'}, {'sub': 'takeover2.xve.io', 'resolution': 'non-existing-bucket.s3.amazonaws.com'}, {'sub': 'takeover3.xve.io', 'resolution': 'totallynonexistingdomain.com'}, {'sub': 'takeover4.xve.io', 'resolution': 'totallynonexistingdomain2.com'}, {'sub': 'takeover5.xve.io', 'resolution': 'takeover4.xve.io'}, {'sub': 'www.xve.io', 'resolution': 'xve.io'}]
result = n.check_takeover(test_domains)