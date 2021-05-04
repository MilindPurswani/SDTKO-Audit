class Cloudflare:
	"""
    This Class will be used to define functions to interact with Cloudflare's API
    We need domain_name, CF_API_KEY as input and we will get the CNAME records from the Cloudflare's API
    """
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		