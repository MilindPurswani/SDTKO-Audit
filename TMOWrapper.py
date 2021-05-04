class TMOWrapper:
	"""
    This Wrapper will be used to call takemeon to check for dangling subdomains pointing to nxdomain
    Define function to check for nxdomain domain and output true or false for each domain indicating whether they are dangling subdomains pointing to nxdomains
    """
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		