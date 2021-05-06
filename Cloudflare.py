import os
import requests
import json

class Cloudflare:
	"""
    This Class will be used to define functions to interact with Cloudflare's API
    We need domain_name, CF_API_KEY as input and we will get the CNAME records from the Cloudflare's API
    """

	# Constructor will check if CF_API_KEY is set or not
	def __init__(self):
		try:
			self.cf_api_key = os.environ['CF_API_KEY']
		except KeyError:
			print("[!] CF_API_KEY not set")
			exit(1)

	# Getting zone id for a particular domain
	def get_zone_id(self, domain):
		url = "https://api.cloudflare.com/client/v4/zones?name="+domain
		headers = {"Authorization" : "Bearer "+self.cf_api_key, "Content-Type" : "application/json"}   
		try:  
			resp = requests.get(url=url, headers=headers)
			json_data = json.loads(resp.text)
			zone_id = json_data['result'][0]['id'] 
		except IndexError as e:
			print("[!] No Zone found for particular domain, are you sure you own this domain?")
			exit(1)
		except json.decoder.JSONDecodeError as e:
			print("[!] Invalid JSON received from cf")
			exit(1)
		return zone_id

	# get cname list for the domain specified
	def get_cname_domains(self, domain):
		domain_list = []
		zone_id = self.get_zone_id(domain)
		url = "https://api.cloudflare.com/client/v4/zones/"+ zone_id +"/dns_records?type=CNAME"
		headers = {"Authorization" : "Bearer "+self.cf_api_key, "Content-Type" : "application/json"}   
		try:
			resp = requests.get(url=url, headers=headers)
			json_data = json.loads(resp.text)
			for i in range(len(json_data['result'])):
				d = {}
				d['sub'] = json_data['result'][i]['name']
				d['resolution'] = json_data['result'][i]['content']
				domain_list.append(d)
		except IndexError as e:
			print("[!] No CNAME records found for this domain")
			exit(1)
		except json.decoder.JSONDecodeError as e:
			print("[!] Invalid JSON received from cf")
			exit(1)
		return domain_list

