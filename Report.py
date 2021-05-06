import pandas as pd
from jinja2 import Environment, FileSystemLoader
import datetime
import os

class Report:
	"""
    Use this class for defining report generation parameters.
    """
	# sub, resolution, name (service), domain_name
	def __init__(self, domain_name):
		self.domain_name = domain_name
		
	# function to generate HTML report from input
	def generate_report_from_template(self, template_name, html_table):
		env = Environment(loader=FileSystemLoader('.'))
		template = env.get_template(template_name)
		# Creating dictionary that holds all the important information for jinja
		template_vars = {"title" : "Subdomain Takeover Scan for "+self.domain_name,
                 "subdomain_takeover_table": html_table,
				 "domain_name": self.domain_name,
				 "date": datetime.datetime.now(datetime.timezone.utc)}
		# Generating HTML template
		html_out = template.render(template_vars)
		return html_out

	# creates a report based on input. If filename is not provided, generates a report in 
	def create_report(self, takeover_list,filename=None):
		if len(takeover_list) == 0:
			return
		report_table = pd.DataFrame.from_records(takeover_list)
		# reodering the columns
		column_reorder = ['sub', 'resolution', 'name']
		report_table = report_table.reindex(columns=column_reorder)
		# renaming the column names 
		report_table.rename(columns={'sub':'Subdomain','resolution':'Resolves to','name':'Vulnerable Service'}, inplace=True)
		# Since we are using BootsWatch, adding classes for good looks
		html_table = report_table.to_html(classes='table table-hover')
		
		# The HTML template for report is stored in report_template.html
		html_out = self.generate_report_from_template("report_template.html",html_table)
		now = datetime.datetime.now()
		# Check if user has supplied a filename as input
		if filename is None:
			filename = self.domain_name+'-'+now.strftime("report/%d-%m-%Y--%H-%M-%S")+'-SDTKO-Audit.html'
		# create directories if not exist
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		# writing HTML report to the filename
		with open(filename, "w") as f:
			f.write(html_out)
		

