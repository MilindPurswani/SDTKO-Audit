import logging
from slack_logger import SlackHandler, SlackFormatter
import os

class Notifications:
	"""
    Use this class to define functions to send notifications to slack or other services as needed.
    """
	
	# check if SLACK_WEBHOOK_URL is set as environment variable or not.
	def __init__(self):
		try:
			self.slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
		except KeyError:
			print("[!] SLACK_WEBHOOK_URL not set")
			exit(1)
	
	def send_debug_notification(self, message):
		logger = logging.getLogger("Update")
		logger.setLevel(logging.DEBUG)
		sh = SlackHandler(username='logger', icon_emoji=':robot_face:', url=self.slack_webhook_url)
		sh.setLevel(logging.DEBUG)
		f = SlackFormatter()
		sh.setFormatter(f)
		logger.addHandler(sh)
		logger.debug(message)
	
	def send_important_notification(self, message):
		logger = logging.getLogger("Important!")
		logger.setLevel(logging.DEBUG)
		sh = SlackHandler(username='logger', icon_emoji=':robot_face:', url=self.slack_webhook_url)
		sh.setLevel(logging.DEBUG)
		f = SlackFormatter()
		sh.setFormatter(f)
		logger.addHandler(sh)
		logger.info(message)

n = Notifications()
n.send_debug_notification("Test")
n.send_important_notification("Important Notification")